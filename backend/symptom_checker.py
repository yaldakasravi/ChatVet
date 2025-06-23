import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

class SymptomChecker:
    def __init__(self, csv_path: str, symptom_col: str = "symptom", suggestion_col: str = "suggestion"):
        """
        Initialize the symptom checker with symptom-suggestion dataset.

        Args:
            csv_path (str): Path to CSV containing symptoms and corresponding suggestions.
            symptom_col (str): Name of the column with symptom descriptions.
            suggestion_col (str): Name of the column with suggested advice.
        """
        self.df = pd.read_csv(csv_path)
        self.symptom_col = symptom_col
        self.suggestion_col = suggestion_col

        # Prepare TF-IDF vectorizer on symptom descriptions
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.symptom_tfidf = self.vectorizer.fit_transform(self.df[self.symptom_col].fillna(""))

    def find_closest_symptoms(self, user_input: str, top_k: int = 3) -> List[Tuple[str, float, str]]:
        """
        Find the closest matching symptoms to the user input.

        Args:
            user_input (str): User's symptom description input.
            top_k (int): Number of top matches to return.

        Returns:
            List of tuples: [(symptom_text, similarity_score, suggestion), ...]
        """
        user_vec = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vec, self.symptom_tfidf).flatten()
        top_indices = similarities.argsort()[::-1][:top_k]

        matches = []
        for idx in top_indices:
            symptom = self.df.iloc[idx][self.symptom_col]
            suggestion = self.df.iloc[idx][self.suggestion_col]
            score = similarities[idx]
            matches.append((symptom, score, suggestion))

        return matches

    def get_suggestions(self, user_input: str, threshold: float = 0.3) -> List[str]:
        """
        Return suggestions for symptoms similar enough to user input.

        Args:
            user_input (str): User's symptom description input.
            threshold (float): Minimum similarity score to consider a match.

        Returns:
            List of suggestion strings.
        """
        matches = self.find_closest_symptoms(user_input)

        filtered_suggestions = [
            suggestion for symptom, score, suggestion in matches if score >= threshold
        ]

        if not filtered_suggestions:
            return ["No close matches found. Please consult a veterinarian for specific advice."]

        return filtered_suggestions


if __name__ == "__main__":
    # Example usage
    checker = SymptomChecker("data/vet_guides.csv", symptom_col="symptom", suggestion_col="suggestion")

    user_query = input("Describe your pet's symptoms: ")
    suggestions = checker.get_suggestions(user_query)

    print("\nSuggested advice based on similar symptoms:")
    for s in suggestions:
        print(f"- {s}")
