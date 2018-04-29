# author: Shane Yu  date: April 8, 2017
from django.core.management.base import BaseCommand, CommandError
from udic_nlp_API.settings_database import uri
from udicTfidf import TFIDF
import logging

logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', filename='buildTfidf.log', level=logging.INFO)

class Command(BaseCommand):
    help = 'use this for build model of tfidf!'
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--lang', type=str)

    def handle(self, *args, **options):
        tfidf = TFIDF(options['lang'], uri)
        logging.info('start build TF-IDF')
        tfidf.build()
        self.stdout.write(self.style.SUCCESS('build tfidf model success!!!'))