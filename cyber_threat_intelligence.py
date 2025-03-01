import os
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import pandas as pd

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
THREAT_REPORT_URL = 'https://api.threatintelligence.com/reports'
SAMPLE_HASHES = ['SHA256_HASH_1', 'SHA256_HASH_2']
API_KEY = 'your_api_key_here'
DATA_DIR = 'data'
OUTPUT_FILE = 'threat_intelligence_report.csv'

class ThreatIntelligence:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def fetch_threat_reports(self):
        response = self.session.get(THREAT_REPORT_URL)
        if response.status_code == 200:
            logging.info('Successfully fetched threat reports.')
            return response.json()
        else:
            logging.error('Failed to fetch threat reports: %s', response.status_code)
            return None
            
    def analyze_reports(self, reports):
        analysis_results = defaultdict(list)
        for report in reports:
            report_date = report.get('date')
            threat_type = report.get('type')
            description = report.get('description')

            analysis_results[threat_type].append({
                'date': report_date,
                'description': description
            })
            
        return analysis_results

    def save_report(self, analysis_results):
        df = pd.DataFrame()
        for threat_type, entries in analysis_results.items():
            for entry in entries:
                df = df.append({
                    'Threat Type': threat_type,
                    'Date': entry['date'],
                    'Description': entry['description']
                }, ignore_index=True)
        
        df.to_csv(OUTPUT_FILE, index=False)
        logging.info('Report saved to %s', OUTPUT_FILE)

    def run(self):
        reports = self.fetch_threat_reports()
        if reports:
            analysis_results = self.analyze_reports(reports)
            self.save_report(analysis_results)

class ArtifactAnalysis:
    def __init__(self, hashes):
        self.hashes = hashes

    def fetch_artifact_info(self):
        results = {}
        for hash_value in self.hashes:
            response = requests.get(f'https://api.threatintelligence.com/artifacts/{hash_value}')
            if response.status_code == 200:
                results[hash_value] = response.json()
            else:
                logging.error('Failed to fetch artifact info for %s: %s', hash_value, response.status_code)
        return results

    def generate_analysis_report(self, artifact_info):
        report = []
        for hash_value, info in artifact_info.items():
            report.append({
                'Hash': hash_value,
                'Type': info.get('type'),
                'Confidence': info.get('confidence'),
                'Last Seen': info.get('last_seen')
            })
        return report

def main():
    logging.info('Starting Cyber Threat Intelligence Tool...')
    
    # Threat Intelligence Collection
    ti = ThreatIntelligence(API_KEY)
    ti.run()
    
    # Artifact Analysis
    artifact_analysis = ArtifactAnalysis(SAMPLE_HASHES)
    artifact_info = artifact_analysis.fetch_artifact_info()
    analysis_report = artifact_analysis.generate_analysis_report(artifact_info)
    
    # Save artifact analysis report
    artifact_df = pd.DataFrame(analysis_report)
    artifact_df.to_csv('artifact_analysis_report.csv', index=False)
    logging.info('Artifact analysis report saved.')

if __name__ == '__main__':
    main()