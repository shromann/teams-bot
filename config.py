#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv

load_dotenv()

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword")
    
    AGENT_URI = "https://adk-default-service-name-575161739761.us-central1.run.app"
    PROMPT_ENDPOINT = f"{AGENT_URI}/run"
    AGENT_NAME = "agents"
    SESSION_ID = "session"
    HEADERS = {
        'Content-Type': 'application/json'
    }
    
    def get_url(user_id):
        return f"{DefaultConfig.AGENT_URI}/apps/{DefaultConfig.AGENT_NAME}/users/{user_id}/sessions/{DefaultConfig.SESSION_ID}"
