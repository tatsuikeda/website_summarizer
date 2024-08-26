import torch
from transformers import BertTokenizer, BertModel
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import numpy as np
from collections import defaultdict

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class AdvancedSummarizer:
    def __init__(self):
        self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.bert_model.to(self.device)
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    def extract_key_sentences(self, text, num_sentences=10):
        sentences = sent_tokenize(text)
        
        # Calculate TF-IDF scores
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Calculate sentence scores
        sentence_scores = tfidf_matrix.sum(axis=1).A1
        
        # Select top sentences
        top_sentences_indices = sentence_scores.argsort()[-num_sentences:][::-1]
        top_sentences = [sentences[i] for i in sorted(top_sentences_indices)]
        
        return top_sentences

    def extract_key_phrases(self, text, num_phrases=5):
        words = word_tokenize(text.lower())
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        phrases = []
        for i in range(len(words) - 1):
            phrases.append((words[i], words[i+1]))
        
        phrase_freq = defaultdict(int)
        for phrase in phrases:
            phrase_freq[phrase] += 1
        
        return sorted(phrase_freq, key=phrase_freq.get, reverse=True)[:num_phrases]

    def structure_summary(self, sentences, key_phrases):
        summary = "Summary:\n\n"
        
        # Add key phrases
        summary += "Key Phrases:\n"
        for phrase in key_phrases:
            summary += f"- {' '.join(phrase)}\n"
        summary += "\n"
        
        # Identify key sections
        sections = {
            "Main Content": [],
            "Features": [],
            "Details": []
        }
        
        for sentence in sentences:
            lower_sentence = sentence.lower()
            if any(phrase[0] in lower_sentence and phrase[1] in lower_sentence for phrase in key_phrases):
                sections["Main Content"].append(sentence)
            elif any(word in lower_sentence for word in ["feature", "benefit", "advantage"]):
                sections["Features"].append(sentence)
            else:
                sections["Details"].append(sentence)
        
        # Create structured summary
        for section, content in sections.items():
            if content:
                summary += f"{section}:\n"
                for sentence in content[:3]:  # Limit to top 3 sentences per section
                    summary += f"- {sentence}\n"
                summary += "\n"
        
        return summary

    def summarize(self, text: str, ratio: float = 0.3) -> str:
        preprocessed_text = self.preprocess_text(text)
        key_sentences = self.extract_key_sentences(preprocessed_text, num_sentences=int(len(sent_tokenize(preprocessed_text)) * ratio))
        key_phrases = self.extract_key_phrases(preprocessed_text)
        structured_summary = self.structure_summary(key_sentences, key_phrases)
        return structured_summary

def create_meta_summary(summaries: dict) -> str:
    meta_summary = "Website Meta-Summary:\n\n"
    for url, summary in summaries.items():
        meta_summary += f"Page: {url}\n{summary}\n\n"
    return meta_summary