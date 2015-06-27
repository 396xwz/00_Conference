#!/usr/bin/env python

"""models.py

Udacity conference server-side Python App Engine data & ProtoRPC models

$Id: models.py,v 1.1 2014/05/24 22:01:10 wesc Exp $

created/forked from conferences.py by wesc on 2014 may 24

"""

__author__ = 'wesc+api@google.com (Wesley Chun)'

import httplib
import endpoints
from protorpc import messages
from google.appengine.ext import ndb


# replaced existing Profile class
class Profile(ndb.Model):
    """Profile -- User profile object"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    teeShirtSize = ndb.StringProperty(default='NOT_SPECIFIED')
    conferenceKeysToAttend = ndb.StringProperty(repeated=True)
    sessionKeysWishlist = ndb.StringProperty(repeated=True)

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)
# needed for conference registration
class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)

class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT


class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- update Profile form message"""
    displayName = messages.StringField(1)
    teeShirtSize = messages.EnumField('TeeShirtSize', 2)


class ProfileForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    teeShirtSize = messages.EnumField('TeeShirtSize', 3)


class TeeShirtSize(messages.Enum):
    """TeeShirtSize -- t-shirt size enumeration value"""
    NOT_SPECIFIED = 1
    XS_M = 2
    XS_W = 3
    S_M = 4
    S_W = 5
    M_M = 6
    M_W = 7
    L_M = 8
    L_W = 9
    XL_M = 10
    XL_W = 11
    XXL_M = 12
    XXL_W = 13
    XXXL_M = 14
    XXXL_W = 15
class Conference(ndb.Model):
    """Conference -- Conference object"""
    name            = ndb.StringProperty(required=True)
    description     = ndb.StringProperty()
    organizerUserId = ndb.StringProperty()
    topics          = ndb.StringProperty(repeated=True)
    city            = ndb.StringProperty()
    startDate       = ndb.DateProperty()
    month           = ndb.IntegerProperty()
    endDate         = ndb.DateProperty()
    maxAttendees    = ndb.IntegerProperty()
    seatsAvailable  = ndb.IntegerProperty()

class ConferenceForm(messages.Message):
    """ConferenceForm -- Conference outbound form message"""
    name            = messages.StringField(1)
    description     = messages.StringField(2)
    organizerUserId = messages.StringField(3)
    topics          = messages.StringField(4, repeated=True)
    city            = messages.StringField(5)
    startDate       = messages.StringField(6)
    month           = messages.IntegerField(7)
    maxAttendees    = messages.IntegerField(8)
    seatsAvailable  = messages.IntegerField(9)
    endDate         = messages.StringField(10)
    websafeKey      = messages.StringField(11)
    organizerDisplayName = messages.StringField(12)
class ConferenceForms(messages.Message):
    """ConferenceForms -- multiple Conference outbound form message"""
    items = messages.MessageField(ConferenceForm, 1, repeated=True)

class ConferenceQueryForm(messages.Message):
    """ConferenceQueryForm -- Conference query inbound form message"""
    field = messages.StringField(1)
    operator = messages.StringField(2)
    value = messages.StringField(3)

class ConferenceQueryForms(messages.Message):
    """ConferenceQueryForms -- multiple ConferenceQueryForm inbound form message"""
    filters = messages.MessageField(ConferenceQueryForm, 1, repeated=True)
class Session(ndb.Model):
    """Session - Each conference can have different sessions"""
    _use_memcache = True

    typeOfSession = ndb.StringProperty(choices=['lecture', 'keynote', 'workshop','sales','technology'])    # possible choices for session
    speaker = ndb.StringProperty(required=True)                                       # speaker of session
    name = ndb.StringProperty(required=True)                                          # title of the session
    duration = ndb.IntegerProperty()                                                  # length in minutes
    startDate = ndb.DateProperty()
    startTime = ndb.TimeProperty()
    highlights = ndb.StringProperty(repeated=True)                                    # one or more arguments for the session
    conference = ndb.KeyProperty(kind='Conference')                                   # the conference to which the session is related

    @classmethod
    def get_sessions_by_conference(cls, conference_key):
        """Returns the Query by conference key"""
        return cls.query(cls.conference == conference_key)

    @classmethod
    def get_sessions_by_speaker(cls, speaker_name):
        """Returns the Query by Speaker"""
        return cls.query(cls.speaker == speaker_name)

class SessionForm(messages.Message):
    """Session Form -- Session outbound form message"""
    name = messages.StringField(1)
    highlights = messages.StringField(2, repeated=True)
    speaker = messages.StringField(3)
    duration = messages.IntegerField(4)
    startDate = messages.StringField(5)
    startTime = messages.StringField(6)
    typeOfSession = messages.StringField(7)
    sessionKey = messages.StringField(8)

class SessionForms(messages.Message):
    """SessionForms -- multiple Sessions outbound form message"""
    items = messages.MessageField(SessionForm, 1, repeated=True)

class FeaturedSpeakerForm(messages.Message):
    speaker = messages.StringField(1)
    sessions = messages.StringField(2, repeated=True)


class FeaturedSpeakerMessage(messages.Message):
    """FeaturedSpeakerMessage - outbound message for featured speakers"""
    featured = messages.MessageField(FeaturedSpeakerForm, 1, repeated=True)
    websafeKey = messages.StringField(2)
