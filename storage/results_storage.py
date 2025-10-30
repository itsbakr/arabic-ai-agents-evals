"""
Results storage for conversation evaluation data
Supports CSV and Supabase
"""

import os
import csv
import json
from datetime import datetime
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
import pandas as pd


class ResultsStorage(ABC):
    """Base class for results storage"""
    
    @abstractmethod
    def save_conversation(self, conversation_data: Dict) -> bool:
        """Save a single conversation result"""
        pass
    
    @abstractmethod
    def save_evaluation(self, evaluation_data: Dict) -> bool:
        """Save evaluation results"""
        pass
    
    @abstractmethod
    def get_all_conversations(self) -> List[Dict]:
        """Get all stored conversations"""
        pass


class JSONStorage(ResultsStorage):
    """JSON file storage for results"""
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize JSON storage
        
        Args:
            output_dir: Directory to store JSON files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.conversations_file = os.path.join(output_dir, "conversations.json")
        self.evaluations_file = os.path.join(output_dir, "evaluations.json")
        
        # Initialize JSON files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize JSON files with empty arrays"""
        if not os.path.exists(self.conversations_file):
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.evaluations_file):
            with open(self.evaluations_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def save_conversation(self, conversation_data: Dict) -> bool:
        """
        Save conversation to JSON
        
        Args:
            conversation_data: Dictionary with conversation results
            
        Returns:
            True if successful
        """
        try:
            # Generate conversation ID
            conversation_id = f"{conversation_data['scenario_id']}_{conversation_data['model_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            timestamp = datetime.now().isoformat()
            
            # Prepare conversation record
            record = {
                'conversation_id': conversation_id,
                'scenario_id': conversation_data['scenario_id'],
                'agent_type': conversation_data['agent_type'],
                'model_name': conversation_data['model_name'],
                'customer_persona': conversation_data.get('customer_persona', ''),
                'customer_goal': conversation_data.get('customer_goal', ''),
                'total_turns': conversation_data['total_turns'],
                'success': conversation_data['success'],
                'end_reason': conversation_data['end_reason'],
                'total_tokens': conversation_data['total_tokens'],
                'total_latency': conversation_data['total_latency'],
                'turns': conversation_data.get('turns', []),
                'timestamp': timestamp
            }
            
            # Read existing data
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            # Append new record
            conversations.append(record)
            
            # Write back
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
            
            print(f"✅ تم حفظ المحادثة في JSON: {conversation_id}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ المحادثة: {e}")
            return False
    
    def save_evaluation(self, evaluation_data: Dict) -> bool:
        """
        Save evaluation results to JSON
        
        Args:
            evaluation_data: Dictionary with evaluation scores
            
        Returns:
            True if successful
        """
        try:
            timestamp = datetime.now().isoformat()
            
            record = {
                'conversation_id': evaluation_data.get('conversation_id', ''),
                'scenario_id': evaluation_data['scenario_id'],
                'model_name': evaluation_data['model_name'],
                'task_completion': evaluation_data.get('task_completion', 0),
                'empathy': evaluation_data.get('empathy', 0),
                'clarity': evaluation_data.get('clarity', 0),
                'cultural_fit': evaluation_data.get('cultural_fit', 0),
                'problem_solving': evaluation_data.get('problem_solving', 0),
                'overall_score': evaluation_data.get('overall_score', 0),
                'evaluator_notes': evaluation_data.get('notes', ''),
                'timestamp': timestamp
            }
            
            # Read existing data
            with open(self.evaluations_file, 'r', encoding='utf-8') as f:
                evaluations = json.load(f)
            
            # Append new record
            evaluations.append(record)
            
            # Write back
            with open(self.evaluations_file, 'w', encoding='utf-8') as f:
                json.dump(evaluations, f, ensure_ascii=False, indent=2)
            
            print(f"✅ تم حفظ التقييم في JSON")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ التقييم: {e}")
            return False
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations from JSON"""
        try:
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ خطأ في قراءة المحادثات: {e}")
            return []


class CSVStorage(ResultsStorage):
    """CSV file storage for results"""
    
    def __init__(self, output_dir: str = "results"):
        """
        Initialize CSV storage
        
        Args:
            output_dir: Directory to store CSV files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.conversations_file = os.path.join(output_dir, "conversations.csv")
        self.turns_file = os.path.join(output_dir, "conversation_turns.csv")
        self.evaluations_file = os.path.join(output_dir, "evaluations.csv")
        
        # Initialize CSV files with headers if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize CSV files with headers"""
        
        # Conversations file
        if not os.path.exists(self.conversations_file):
            with open(self.conversations_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'conversation_id', 'scenario_id', 'agent_type', 'model_name',
                    'customer_persona', 'customer_goal', 'total_turns', 'success',
                    'end_reason', 'total_tokens', 'total_latency', 'timestamp'
                ])
                writer.writeheader()
        
        # Turns file
        if not os.path.exists(self.turns_file):
            with open(self.turns_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'conversation_id', 'turn_number', 'customer_message',
                    'agent_message', 'customer_tokens', 'agent_tokens',
                    'turn_latency', 'timestamp'
                ])
                writer.writeheader()
        
        # Evaluations file
        if not os.path.exists(self.evaluations_file):
            with open(self.evaluations_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'conversation_id', 'scenario_id', 'model_name',
                    'task_completion', 'empathy', 'clarity', 'cultural_fit',
                    'problem_solving', 'overall_score', 'evaluator_notes',
                    'timestamp'
                ])
                writer.writeheader()
    
    def save_conversation(self, conversation_data: Dict) -> bool:
        """
        Save conversation to CSV
        
        Args:
            conversation_data: Dictionary with conversation results
            
        Returns:
            True if successful
        """
        try:
            # Generate conversation ID
            conversation_id = f"{conversation_data['scenario_id']}_{conversation_data['model_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            timestamp = datetime.now().isoformat()
            
            # Save conversation metadata
            with open(self.conversations_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'conversation_id', 'scenario_id', 'agent_type', 'model_name',
                    'customer_persona', 'customer_goal', 'total_turns', 'success',
                    'end_reason', 'total_tokens', 'total_latency', 'timestamp'
                ])
                writer.writerow({
                    'conversation_id': conversation_id,
                    'scenario_id': conversation_data['scenario_id'],
                    'agent_type': conversation_data['agent_type'],
                    'model_name': conversation_data['model_name'],
                    'customer_persona': conversation_data.get('customer_persona', ''),
                    'customer_goal': conversation_data.get('customer_goal', ''),
                    'total_turns': conversation_data['total_turns'],
                    'success': conversation_data['success'],
                    'end_reason': conversation_data['end_reason'],
                    'total_tokens': conversation_data['total_tokens'],
                    'total_latency': conversation_data['total_latency'],
                    'timestamp': timestamp
                })
            
            # Save conversation turns
            with open(self.turns_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'conversation_id', 'turn_number', 'customer_message',
                    'agent_message', 'customer_tokens', 'agent_tokens',
                    'turn_latency', 'timestamp'
                ])
                for turn in conversation_data.get('turns', []):
                    writer.writerow({
                        'conversation_id': conversation_id,
                        'turn_number': turn['turn'],
                        'customer_message': turn['customer'],
                        'agent_message': turn['agent'],
                        'customer_tokens': turn.get('customer_tokens', 0),
                        'agent_tokens': turn.get('agent_tokens', 0),
                        'turn_latency': turn.get('latency', 0),
                        'timestamp': timestamp
                    })
            
            print(f"✅ تم حفظ المحادثة في CSV: {conversation_id}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ المحادثة: {e}")
            return False
    
    def save_evaluation(self, evaluation_data: Dict) -> bool:
        """
        Save evaluation results to CSV
        
        Args:
            evaluation_data: Dictionary with evaluation scores
            
        Returns:
            True if successful
        """
        try:
            timestamp = datetime.now().isoformat()
            
            with open(self.evaluations_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'conversation_id', 'scenario_id', 'model_name',
                    'task_completion', 'empathy', 'clarity', 'cultural_fit',
                    'problem_solving', 'overall_score', 'evaluator_notes',
                    'timestamp'
                ])
                writer.writerow({
                    'conversation_id': evaluation_data.get('conversation_id', ''),
                    'scenario_id': evaluation_data['scenario_id'],
                    'model_name': evaluation_data['model_name'],
                    'task_completion': evaluation_data.get('task_completion', 0),
                    'empathy': evaluation_data.get('empathy', 0),
                    'clarity': evaluation_data.get('clarity', 0),
                    'cultural_fit': evaluation_data.get('cultural_fit', 0),
                    'problem_solving': evaluation_data.get('problem_solving', 0),
                    'overall_score': evaluation_data.get('overall_score', 0),
                    'evaluator_notes': evaluation_data.get('notes', ''),
                    'timestamp': timestamp
                })
            
            print(f"✅ تم حفظ التقييم في CSV")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ التقييم: {e}")
            return False
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations from CSV"""
        try:
            df = pd.read_csv(self.conversations_file)
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ خطأ في قراءة المحادثات: {e}")
            return []
    
    def export_summary(self, output_file: str = None) -> bool:
        """
        Export summary statistics to Excel
        
        Args:
            output_file: Output Excel file path
            
        Returns:
            True if successful
        """
        try:
            if output_file is None:
                output_file = os.path.join(self.output_dir, f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            
            # Read data
            conversations_df = pd.read_csv(self.conversations_file)
            evaluations_df = pd.read_csv(self.evaluations_file)
            
            # Create summary
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Conversations summary
                conversations_df.to_excel(writer, sheet_name='Conversations', index=False)
                
                # Evaluations summary
                if not evaluations_df.empty:
                    evaluations_df.to_excel(writer, sheet_name='Evaluations', index=False)
                
                # Model comparison
                model_summary = conversations_df.groupby('model_name').agg({
                    'total_turns': 'mean',
                    'total_tokens': 'mean',
                    'total_latency': 'mean',
                    'success': 'sum'
                }).reset_index()
                model_summary.to_excel(writer, sheet_name='Model_Comparison', index=False)
            
            print(f"✅ تم تصدير الملخص: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في التصدير: {e}")
            return False


class SupabaseStorage(ResultsStorage):
    """Supabase database storage for results"""
    
    def __init__(self, url: str, key: str):
        """
        Initialize Supabase storage
        
        Args:
            url: Supabase project URL
            key: Supabase anon key
        """
        try:
            from supabase import create_client, Client
            self.client: Client = create_client(url, key)
            print("✅ متصل بـ Supabase")
        except ImportError:
            raise ImportError("يرجى تثبيت supabase: pip install supabase")
        except Exception as e:
            raise Exception(f"خطأ في الاتصال بـ Supabase: {e}")
    
    def save_conversation(self, conversation_data: Dict) -> bool:
        """
        Save conversation to Supabase
        
        Args:
            conversation_data: Dictionary with conversation results
            
        Returns:
            True if successful
        """
        try:
            # Generate conversation ID
            conversation_id = f"{conversation_data['scenario_id']}_{conversation_data['model_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save conversation metadata
            conversation_record = {
                'conversation_id': conversation_id,
                'scenario_id': conversation_data['scenario_id'],
                'agent_type': conversation_data['agent_type'],
                'model_name': conversation_data['model_name'],
                'customer_persona': conversation_data.get('customer_persona', ''),
                'customer_goal': conversation_data.get('customer_goal', ''),
                'total_turns': conversation_data['total_turns'],
                'success': conversation_data['success'],
                'end_reason': conversation_data['end_reason'],
                'total_tokens': conversation_data['total_tokens'],
                'total_latency': conversation_data['total_latency'],
                'created_at': datetime.now().isoformat()
            }
            
            self.client.table('conversations').insert(conversation_record).execute()
            
            # Save conversation turns
            turns_records = [
                {
                    'conversation_id': conversation_id,
                    'turn_number': turn['turn'],
                    'customer_message': turn['customer'],
                    'agent_message': turn['agent'],
                    'customer_tokens': turn.get('customer_tokens', 0),
                    'agent_tokens': turn.get('agent_tokens', 0),
                    'turn_latency': turn.get('latency', 0),
                    'created_at': datetime.now().isoformat()
                }
                for turn in conversation_data.get('turns', [])
            ]
            
            if turns_records:
                self.client.table('conversation_turns').insert(turns_records).execute()
            
            print(f"✅ تم حفظ المحادثة في Supabase: {conversation_id}")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ المحادثة في Supabase: {e}")
            return False
    
    def save_evaluation(self, evaluation_data: Dict) -> bool:
        """
        Save evaluation results to Supabase
        
        Args:
            evaluation_data: Dictionary with evaluation scores
            
        Returns:
            True if successful
        """
        try:
            evaluation_record = {
                'conversation_id': evaluation_data.get('conversation_id', ''),
                'scenario_id': evaluation_data['scenario_id'],
                'model_name': evaluation_data['model_name'],
                'task_completion': evaluation_data.get('task_completion', 0),
                'empathy': evaluation_data.get('empathy', 0),
                'clarity': evaluation_data.get('clarity', 0),
                'cultural_fit': evaluation_data.get('cultural_fit', 0),
                'problem_solving': evaluation_data.get('problem_solving', 0),
                'overall_score': evaluation_data.get('overall_score', 0),
                'evaluator_notes': evaluation_data.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }
            
            self.client.table('evaluations').insert(evaluation_record).execute()
            
            print(f"✅ تم حفظ التقييم في Supabase")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في حفظ التقييم في Supabase: {e}")
            return False
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations from Supabase"""
        try:
            response = self.client.table('conversations').select('*').execute()
            return response.data
        except Exception as e:
            print(f"❌ خطأ في قراءة المحادثات من Supabase: {e}")
            return []


def get_storage(storage_mode: str = "json", **kwargs) -> ResultsStorage:
    """
    Factory function to get appropriate storage instance
    
    Args:
        storage_mode: 'json', 'csv', 'supabase', or 'both'
        **kwargs: Additional arguments for storage initialization
        
    Returns:
        Storage instance
    """
    if storage_mode == "json":
        return JSONStorage(output_dir=kwargs.get('output_dir', 'results'))
    elif storage_mode == "csv":
        return CSVStorage(output_dir=kwargs.get('output_dir', 'results'))
    elif storage_mode == "supabase":
        return SupabaseStorage(
            url=kwargs.get('supabase_url'),
            key=kwargs.get('supabase_key')
        )
    elif storage_mode == "both":
        # Return a wrapper that saves to both JSON and Supabase
        class DualStorage(ResultsStorage):
            def __init__(self):
                self.json = JSONStorage(output_dir=kwargs.get('output_dir', 'results'))
                self.supabase = SupabaseStorage(
                    url=kwargs.get('supabase_url'),
                    key=kwargs.get('supabase_key')
                )
            
            def save_conversation(self, conversation_data: Dict) -> bool:
                json_success = self.json.save_conversation(conversation_data)
                supabase_success = self.supabase.save_conversation(conversation_data)
                return json_success and supabase_success
            
            def save_evaluation(self, evaluation_data: Dict) -> bool:
                json_success = self.json.save_evaluation(evaluation_data)
                supabase_success = self.supabase.save_evaluation(evaluation_data)
                return json_success and supabase_success
            
            def get_all_conversations(self) -> List[Dict]:
                return self.supabase.get_all_conversations()  # Prefer Supabase for reads
        
        return DualStorage()
    else:
        raise ValueError(f"Unsupported storage mode: {storage_mode}")

