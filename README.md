# Email Triage Environment (OpenEnv)

## Overview

This project implements a real-world email triage environment using the OpenEnv framework.

The agent is required to:
1. Classify incoming emails
2. Extract user intent
3. Generate an appropriate reply

---

## Tasks

### 1. Classification (Easy)
Classify the email into one of:
- spam
- important
- support

### 2. Intent Extraction (Medium)
Identify the user's intent:
- pricing inquiry
- complaint
- booking
- general question

### 3. Reply Generation (Hard)
Generate a suitable response to the email.

---

## Environment Design

## Action Space

EmailTriageAction:
- action_type: "classification" | "intent" | "reply"
- content: string

---

## Observation Space

EmailTriageObservation:
- email_text: str
- current_stage: str
- history: list
- reward: float
- done: bool

---

## State

EmailTriageState:
- email_text
- true_classification
- true_intent
- true_reply
- current_stage

---

## Reward System

- Classification → 0.3  
- Intent → 0.3  
- Reply → 0.4  

Partial credit is given for acceptable replies.

---

## Running the Environment

### 1. Install dependencies

```bash
pip install fastapi uvicorn openenv-core

