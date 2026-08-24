"""
Architectural Decoupling & Zero-Leakage Verification Suite
Ensures that all application subsystems remain strictly decoupled with zero code leakage.
"""
import unittest
import importlib
import inspect
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestArchitecturalDecoupling(unittest.TestCase):
    """Rigorous verification that subsystems maintain clean boundary isolation."""

    def test_scraper_subsystem_has_no_llm_or_db_dependencies(self):
        """Scraper & Scrapling engine must be pure parsers with no LLM or Database imports."""
        import scraper
        import scrapling_engine
        
        scraper_src = inspect.getsource(scraper)
        scrapling_src = inspect.getsource(scrapling_engine)
        
        self.assertNotIn('LLMClient', scraper_src, 'Scraper must not depend on LLMClient')
        self.assertNotIn('init_db', scraper_src, 'Scraper must not depend on database')
        self.assertNotIn('LLMClient', scrapling_src, 'Scrapling engine must not depend on LLMClient')
        self.assertNotIn('database', scrapling_src, 'Scrapling engine must not depend on database')

    def test_validation_layer_is_pure_and_stateless(self):
        """Validation layer and fact checker must be pure verification functions."""
        import validation_layer
        import fact_checker
        import linter
        
        val_src = inspect.getsource(validation_layer)
        fact_src = inspect.getsource(fact_checker)
        lint_src = inspect.getsource(linter)
        
        self.assertNotIn('LLMClient', val_src, 'Validation layer must be deterministic without LLM calls')
        self.assertNotIn('save_output', val_src, 'Validation layer must not write to DB')
        self.assertNotIn('LLMClient', lint_src, 'Linter must be deterministic without LLM calls')

    def test_content_studio_isolated_from_19_section_schema(self):
        """Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline."""
        from agents import content_creator_agent
        src = inspect.getsource(content_creator_agent)
        
        self.assertNotIn('process_package', src, 'Content Creator Agent must not call batch pipeline')
        self.assertNotIn('SectionedContent', src, 'Content Creator Agent must not depend on 19-section schema')
        self.assertNotIn('save_output', src, 'Content Creator Agent must not perform DB operations directly')

    def test_19_section_pipeline_isolated_from_content_studio(self):
        """19-Section Pipeline must be decoupled from AI Studio."""
        import pipeline
        src = inspect.getsource(pipeline)
        
        self.assertNotIn('content_creator_agent', src, 'Pipeline must not import content_creator_agent')
        self.assertNotIn('_generate_long_form_blog', src, 'Pipeline must not call blog generator')

    def test_llm_client_has_no_shared_mutable_lockout_state(self):
        """LLMClient instances must be stateless between requests with zero shared lockout dictionaries."""
        from llm_client import LLMClient
        client1 = LLMClient()
        client2 = LLMClient()
        
        self.assertFalse(hasattr(client1, '_failed_providers'), 'LLMClient must not have global lockout dictionary')
        self.assertFalse(hasattr(client2, '_failed_providers'), 'LLMClient must not have global lockout dictionary')

    def test_public_apis_enricher_is_standalone(self):
        """Public APIs enricher must work autonomously without pipeline or studio dependencies."""
        import public_apis_enricher
        src = inspect.getsource(public_apis_enricher)
        self.assertNotIn('process_package', src)
        self.assertNotIn('content_creator_agent', src)


if __name__ == '__main__':
    unittest.main()