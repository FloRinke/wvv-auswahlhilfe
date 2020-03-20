from django.core.management.base import BaseCommand
from django.utils.text import slugify
import argparse
import sys
import csv
from projects.models import *

class Command(BaseCommand):
    help = "Import List of projects"

    def _try_challenge(self, data):
        #print("Query for Challenge '{}'".format(data))
        try:
            obj = Challenge.objects.get(title=data)
            #print(" skip, existing")
        except Challenge.DoesNotExist as e:
            obj = Challenge(title=data)
            obj.slug = slugify(data.split(':')[0])
            obj.save()
            print("Created Challenge '[{}]{}'".format(obj.slug, data))
            #print("  create in db")
        return obj

    def _try_slackchannel(self, data):
        #print("Query for SlackChannel '{}'".format(data))
        try:
            obj = SlackChannel.objects.get(name=data)
            #print(" skip, existing")
        except SlackChannel.DoesNotExist as e:
            obj = SlackChannel(name=data)
            obj.save()
            print("Created SlackChannel '{}'".format(data))
            #print("  create in db")
        return obj

    def _try_category(self, data):
        #print("Query for Category '{}'".format(data))
        if data == 'checked':
            data = "Ministeriumsprojekt"
        try:
            obj = Category.objects.get(description=data)
            #print(" skip, existing")
        except Category.DoesNotExist as e:
            obj = Category(description=data)
            obj.slug = slugify(data.split(' ')[0])
            if obj.slug == "medizinische":
                obj.slug = "med_versorgung"
            elif obj.slug == "deutsche":
                obj.slug = "wirtschaft"
            elif obj.slug == "leben":
                obj.slug = "quarantaene"
            obj.save()
            print("Created Category '[{}]{}'".format(obj.slug, data))
            #print("  create in db")
        return obj

    def _get_categories(self, data):
        categories = list()
        relevant = data[8:15]
        relevant.append(data[17])
        for item in relevant:
            if len(item) > 0:
                #print("  match[{}]: {}".format(len(item),item))
                categories.append(self._try_category(item))
        return categories

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('r'), default=sys.stdin)

    def handle(self, *args, **kwargs):
        reader = csv.reader(kwargs['filename'])
        headers = next(reader)

        for item in headers[8:15]:
            self._try_category(item)
        for item in headers[17:]:
            self._try_category(item)

        cnt_new = 0
        cnt_skip = 0

        for line in reader:
            ch = line[0]
            title = line[1]
            prob = line[2]
            expl = line[3]
            idea = line[4]
            affected = line[5]
            stake = line[6]
            slack = line[7]

            challenge = self._try_challenge(ch)
            slack_channel = self._try_slackchannel(slack)

            #check duplicate
            try:
                Project.objects.get(challenge=challenge, slack=slack_channel, title=title, problem=prob)
                #print("skip {}".format(title))
                cnt_skip += 1
                continue
            except Project.DoesNotExist:
                pass
            except Project.MultipleObjectsReturned as e:
                print("Exception '{}' for '{}'".format(e, title))
                raise e

            cnt_new += 1
            project = Project()
            project.challenge = challenge
            project.title = title
            project.problem = prob
            project.explanation = expl
            project.idea = idea
            project.affected = affected
            project.stakeholder = stake
            project.slack = slack_channel
            project.save()
            for item in self._get_categories(line):
                #print("add cat '{}'".format(item))
                project.category.add(item)
            project.save()
            
        print("Imported {} new, skipped {} old".format(cnt_new, cnt_skip))



