import logging
 
from django.conf import settings
from django.contrib.auth.models import User
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from News.models import Article
 
 
logger = logging.getLogger(__name__)
 
 
def my_job():
    articles = Article.objects.all()
    users = User.objects.all()
    subject = 'Weekly update'
    for user in users:
        message = render_to_string('email/weekly_update.html', {'articles': articles,'user': user})
        email_message = EmailMessage(subject, message, to=[user.email])
        email_message.send()
 

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='mon', hour='10'),
            id="my_job", 
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")