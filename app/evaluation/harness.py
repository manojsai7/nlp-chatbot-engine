"""Evaluation harness for testing chatbot performance"""
import logging
from typing import List, Dict, Any
import statistics

logger = logging.getLogger(__name__)


class EvaluationHarness:
    """Evaluate chatbot performance on test conversations"""
    
    def __init__(self):
        """Initialize evaluation harness"""
        self.test_conversations = self._load_test_conversations()
        
    def _load_test_conversations(self) -> List[Dict[str, Any]]:
        """Load test conversation scenarios
        
        Returns:
            List of test conversation dictionaries
        """
        return [
            {
                "name": "Greeting Flow",
                "turns": [
                    {
                        "user": "Hello!",
                        "expected_intent": "greeting",
                        "min_confidence": 0.7
                    },
                    {
                        "user": "How are you?",
                        "expected_intent": "small_talk",
                        "min_confidence": 0.6
                    },
                    {
                        "user": "Goodbye",
                        "expected_intent": "farewell",
                        "min_confidence": 0.7
                    }
                ]
            },
            {
                "name": "Help Request",
                "turns": [
                    {
                        "user": "I need help with something",
                        "expected_intent": "help",
                        "min_confidence": 0.7
                    },
                    {
                        "user": "Can you assist me?",
                        "expected_intent": "request",
                        "min_confidence": 0.6
                    }
                ]
            },
            {
                "name": "Question Flow",
                "turns": [
                    {
                        "user": "What is the weather like?",
                        "expected_intent": "question",
                        "min_confidence": 0.7
                    },
                    {
                        "user": "Where can I find more information?",
                        "expected_intent": "question",
                        "min_confidence": 0.7
                    }
                ]
            },
            {
                "name": "Complaint Handling",
                "turns": [
                    {
                        "user": "I have a complaint about the service",
                        "expected_intent": "complaint",
                        "min_confidence": 0.7
                    },
                    {
                        "user": "This is not working properly",
                        "expected_intent": "complaint",
                        "min_confidence": 0.6
                    }
                ]
            }
        ]
    
    def evaluate_intent_classification(self, classifier) -> Dict[str, Any]:
        """Evaluate intent classification accuracy
        
        Args:
            classifier: Intent classifier instance
            
        Returns:
            Evaluation metrics
        """
        correct = 0
        total = 0
        confidences = []
        results = []
        
        for conversation in self.test_conversations:
            conv_name = conversation["name"]
            
            for turn in conversation["turns"]:
                total += 1
                user_input = turn["user"]
                expected_intent = turn["expected_intent"]
                min_confidence = turn["min_confidence"]
                
                # Classify
                predicted_intent, confidence = classifier.classify(user_input)
                confidences.append(confidence)
                
                # Check if correct
                is_correct = (
                    predicted_intent == expected_intent and
                    confidence >= min_confidence
                )
                
                if is_correct:
                    correct += 1
                
                results.append({
                    "conversation": conv_name,
                    "input": user_input,
                    "expected": expected_intent,
                    "predicted": predicted_intent,
                    "confidence": confidence,
                    "correct": is_correct
                })
        
        accuracy = correct / total if total > 0 else 0
        avg_confidence = statistics.mean(confidences) if confidences else 0
        
        metrics = {
            "accuracy": accuracy,
            "correct": correct,
            "total": total,
            "average_confidence": avg_confidence,
            "results": results
        }
        
        logger.info(f"Intent classification evaluation: {accuracy:.2%} accuracy")
        return metrics
    
    def evaluate_entity_extraction(self, extractor) -> Dict[str, Any]:
        """Evaluate entity extraction
        
        Args:
            extractor: Entity extractor instance
            
        Returns:
            Evaluation metrics
        """
        test_cases = [
            {
                "text": "My email is john@example.com",
                "expected_entities": ["EMAIL"]
            },
            {
                "text": "Call me at 555-123-4567",
                "expected_entities": ["PHONE"]
            },
            {
                "text": "I live in New York City",
                "expected_entities": ["GPE"]  # Geopolitical entity (if using spaCy)
            }
        ]
        
        results = []
        total_expected = 0
        total_found = 0
        
        for case in test_cases:
            text = case["text"]
            expected = case["expected_entities"]
            
            entities = extractor.extract(text)
            found_labels = [e.label for e in entities]
            
            total_expected += len(expected)
            total_found += len(entities)
            
            results.append({
                "text": text,
                "expected": expected,
                "found": found_labels,
                "count": len(entities)
            })
        
        metrics = {
            "test_cases": len(test_cases),
            "total_expected": total_expected,
            "total_found": total_found,
            "results": results
        }
        
        logger.info(f"Entity extraction evaluation: {total_found} entities found")
        return metrics
    
    def run_full_evaluation(self) -> Dict[str, Any]:
        """Run full evaluation suite
        
        Returns:
            Complete evaluation results
        """
        from app.nlp.intent_classifier import get_intent_classifier
        from app.nlp.entity_extractor import get_entity_extractor
        
        logger.info("Starting full evaluation suite")
        
        # Evaluate intent classification
        classifier = get_intent_classifier()
        intent_metrics = self.evaluate_intent_classification(classifier)
        
        # Evaluate entity extraction
        extractor = get_entity_extractor()
        entity_metrics = self.evaluate_entity_extraction(extractor)
        
        results = {
            "intent_classification": intent_metrics,
            "entity_extraction": entity_metrics,
            "summary": {
                "intent_accuracy": intent_metrics["accuracy"],
                "entities_found": entity_metrics["total_found"]
            }
        }
        
        logger.info("Evaluation complete")
        return results


# Global instance
_evaluator = None


def get_evaluator() -> EvaluationHarness:
    """Get or create the global evaluator instance"""
    global _evaluator
    if _evaluator is None:
        _evaluator = EvaluationHarness()
    return _evaluator
