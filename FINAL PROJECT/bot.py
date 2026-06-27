#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

# Disable system proxy
os.environ['NO_PROXY'] = '*'

from telegram import Update #type:ignore
from telegram.ext import Application, CommandHandler, ContextTypes  #type:ignore
from config import BOT_TOKEN
from handlers import CommandHandlers
from db import Database

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the bot"""
    
    proxy_url = None
    
    if proxy_url:
        logger.info(f"Using proxy: {proxy_url}")
        application = Application.builder()\
            .token(BOT_TOKEN)\
            .proxy(proxy_url)\
            .build()
    else:
        logger.info("No proxy configured - using direct connection (or VPN)")
        application = Application.builder().token(BOT_TOKEN).build()
    
    # Initialize database
    db = Database()
    logger.info("Database initialized")
    
    # Register command handlers
    application.add_handler(CommandHandler('start', CommandHandlers.start))
    application.add_handler(CommandHandler('help', CommandHandlers.help))
    application.add_handler(CommandHandler('about', CommandHandlers.about))
    application.add_handler(CommandHandler('joke', CommandHandlers.joke))
    application.add_handler(CommandHandler('weather', CommandHandlers.weather))
    application.add_handler(CommandHandler('todo', CommandHandlers.todo))
    application.add_handler(CommandHandler('addtodo', CommandHandlers.addtodo))
    application.add_handler(CommandHandler('done', CommandHandlers.done))
    application.add_handler(CommandHandler('deltodo', CommandHandlers.deltodo))
    
    # Start the bot
    logger.info("Starting bot...")
    print("✅ Bot started! Press Ctrl+C to stop.")
    
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped.")
    finally:
        db.close()

if __name__ == '__main__':
    main()