from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ecp_validator", ROOT / "scripts" / "validate_ecp_assets.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class EcpAssetValidatorTests(unittest.TestCase):
    def write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def codes(self, report, bucket="errors"):
        return {x["code"] for x in report[bucket]}

    def test_minimal_ontology_is_locally_valid(self):
        with tempfile.TemporaryDirectory() as td:
            p = self.write(Path(td), "ontology.ttl", '''
@prefix ex: <https://example.test/ubo#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.test/ubo> a owl:Ontology .
ex:Subject a owl:Class ; rdfs:label "主体" .
ex:Organization a owl:Class ; rdfs:subClassOf ex:Subject ; rdfs:label "组织" .
ex:owns a owl:ObjectProperty ; rdfs:domain ex:Subject ; rdfs:range ex:Organization .
ex:ratio a owl:DatatypeProperty ; rdfs:domain ex:Subject ; rdfs:range xsd:decimal .
''')
            report = mod.validate_path(p)
            self.assertEqual(report["summary"]["status"], "LOCALLY_VALID")
            self.assertFalse(report["summary"]["releaseReady"])
            self.assertTrue(report["summary"]["ecpPreflightRequired"])

    def test_owl_restriction_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = self.write(Path(td), "bad.ttl", '''
@prefix ex: <https://example.test/x#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
<https://example.test/x> a owl:Ontology .
ex:A a owl:Class ; rdfs:subClassOf [ a owl:Restriction ; owl:onProperty ex:p ] .
ex:p a owl:ObjectProperty .
''')
            report = mod.validate_path(p)
            self.assertEqual(report["summary"]["status"], "INVALID")
            self.assertTrue({"ONTOLOGY_BNODE", "ONTOLOGY_UNSUPPORTED"}.intersection(self.codes(report)))

    def test_evaluation_definition_without_compiler_contract_requires_preflight(self):
        with tempfile.TemporaryDirectory() as td:
            p = self.write(Path(td), "evaluation.json", json.dumps({
                "apiVersion": "enterprise-cognitive/evaluation-definition/v1",
                "spec": {"name": "draft"}
            }))
            report = mod.validate_path(p)
            self.assertEqual(report["summary"]["status"], "LOCALLY_VALID")
            self.assertIn("EVALUATION_DRAFT", self.codes(report, "warnings"))
            self.assertTrue(report["summary"]["ecpPreflightRequired"])

    def test_action_policy_rejects_endpoint_key(self):
        with tempfile.TemporaryDirectory() as td:
            p = self.write(Path(td), "action.json", json.dumps({
                "kind": "ActionPolicy",
                "endpoint": "https://forbidden.invalid"
            }))
            report = mod.validate_path(p)
            self.assertEqual(report["summary"]["status"], "INVALID")
            self.assertIn("BANNED_CONFIG", self.codes(report))

    def test_workspace_v1_with_scope_files_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "scopes").mkdir()
            self.write(root, "scopes/example.json", "{}")
            manifest = {
                "schemaVersion": 1,
                "kind": "ECP_SEMANTIC_WORKSPACE_PACKAGE",
                "bundleFormat": "enterprise-cognitive/semantic-workspace-package/1.0.0",
                "semanticProfileId": mod.PROFILE_ID,
                "semanticProfileDigest": mod.PROFILE_DIGEST,
                "ontology": {"path": "ontology.ttl", "sourceDigest": "sha256:" + "0"*64, "mediaType": "text/turtle"},
                "mapping": {"path": "mapping.json", "sourceDigest": "sha256:" + "0"*64, "mediaType": "application/json", "ontologySourceDigest": "sha256:" + "0"*64},
                "ruleSet": {"manifestPath": "rules/manifest.json", "sourceDigest": "sha256:" + "0"*64},
                "schemas": []
            }
            self.write(root, "manifest.json", json.dumps(manifest))
            report = mod.validate_path(root)
            self.assertIn("SCOPE_REQUIRES_V2", self.codes(report))


if __name__ == "__main__":
    unittest.main()
