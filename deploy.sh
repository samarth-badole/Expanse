#!/bin/bash
# Quick deploy script - install Railway CLI first: pip install railway-cli

cd "$(dirname "$0")"
railway login
railway init --name expanse-expense-tracker
railway up
