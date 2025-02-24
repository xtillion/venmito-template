from etl_pipeline.aggregators.people_promotions_aggregator import PeoplePromotionsAggregator
from etl_pipeline.aggregators.people_transactions_aggregator import PeopleTransactionsAggregator

class PromotionSuggestionAnalyzer:
    def __init__(self, min_acceptance_rate=60, low_acceptance_threshold=30):
        self.promotions_aggregator = PeoplePromotionsAggregator()
        self.people_transactions_aggregator = PeopleTransactionsAggregator()
        self.min_acceptance_rate = min_acceptance_rate  # Focus on groups with 60%+ engagement
        self.low_acceptance_threshold = low_acceptance_threshold  # Flag groups with <30% engagement

    def generate_suggestion_message(self, metric_type, value, accepted_count, declined_count, acceptance_ratio, underrepresented=False):
        """Generate a clear suggestion message focusing on engagement trends."""
        total = accepted_count + declined_count

        if underrepresented:
            return (f"Customers in {value} showed very low engagement. Only {accepted_count} out of {total} accepted ({acceptance_ratio:.2f}%). "
                    f"Consider adjusting strategies for {value}-based customers.")
        
        if metric_type == "country":
            return (f"Customers in {value} responded well. {accepted_count} out of {total} accepted ({acceptance_ratio:.2f}%). "
                    f"Consider prioritizing {value}-based customers.")

        if metric_type == "device":
            return (f"{value} users responded well. {accepted_count} out of {total} accepted ({acceptance_ratio:.2f}%). "
                    f"Consider increasing focus on {value} users.")

    def analyze_acceptance_criteria(self, accepted_counts, declined_counts, metric_type, total_accepted):
        """Analyzes response trends and suggests where to focus marketing efforts."""
        suggestions = []
        
        for key, accepted_count in accepted_counts.items():
            declined_count = declined_counts.get(key, 0)  # Default to 0 if key not in declined data
            total = accepted_count + declined_count

            if total == 0:
                continue  # Skip if no data

            acceptance_ratio = (accepted_count / total) * 100  # % of people who responded positively
            
            # **Prioritize groups with high engagement (above 60%)**
            if acceptance_ratio >= self.min_acceptance_rate:
                suggestion_message = self.generate_suggestion_message(metric_type, key, accepted_count, declined_count, acceptance_ratio)
                suggestions.append({
                    'metric_value': key,
                    'metric_count_by_accepted_promotions': accepted_count,
                    'metric_count_by_declined_promotions': declined_count,
                    'acceptance_ratio': acceptance_ratio,
                    'suggestion': suggestion_message
                })

            # **Highlight underrepresented groups ONLY if their response rate is very low (below 30%)**
            elif acceptance_ratio < self.low_acceptance_threshold:
                suggestion_message = self.generate_suggestion_message(metric_type, key, accepted_count, declined_count, acceptance_ratio, underrepresented=True)
                suggestions.append({
                    'metric_value': key,
                    'metric_count_by_accepted_promotions': accepted_count,
                    'metric_count_by_declined_promotions': declined_count,
                    'acceptance_ratio': acceptance_ratio,
                    'suggestion': suggestion_message
                })

        # **Ensure a valid JSON structure is always returned**
        return {'metric_type': metric_type, 'metric_values': suggestions} if suggestions else {'metric_type': metric_type, 'metric_values': []}

    def suggest_improvements(self, promotion_name=None):
        """Analyzes positive trends based on country and devices for accepted promotions."""
        accepted = self.promotions_aggregator.get_people_with_accepted_promotions()
        declined = self.promotions_aggregator.get_people_with_denied_promotions()

        if promotion_name is not None:
            accepted = accepted[accepted['promotion'] == promotion_name]
            declined = declined[declined['promotion'] == promotion_name]

        # Calculate total accepted count
        total_accepted = accepted.shape[0]

        # Analyze devices and country patterns
        accepted_devices = accepted['devices'].explode().value_counts().to_dict()
        declined_devices = declined['devices'].explode().value_counts().to_dict()
        accepted_countries = accepted['country'].value_counts().to_dict()
        declined_countries = declined['country'].value_counts().to_dict()

        device_analysis = self.analyze_acceptance_criteria(accepted_devices, declined_devices, 'device', total_accepted)
        country_analysis = self.analyze_acceptance_criteria(accepted_countries, declined_countries, 'country', total_accepted)

        return [device_analysis, country_analysis]
