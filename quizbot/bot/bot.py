"""
Telegram bot to create and attempt to quizzes.
"""

import os
import logging

from telegram.ext import Application,Updater,ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
import quizbot.bot.create_quiz as createQuiz
import quizbot.bot.attempt_quiz as attemptQuiz
import quizbot.bot.edit_quiz as editQuiz

from dotenv import load_dotenv

load_dotenv()

# Heroku Port
PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def print_help(update, _):
    """Send a message when the command /help is issued."""
    update.message.reply_TEXT(
        'Hey! 🙋‍♂️ How can I help you?\n'
    )
    update.message.reply_TEXT(
        'What QuizBot is? 😃\n\n'
        'With QuizBot you can create quizzes with different question types. 🧐 You can\n'
        '- ask for a number,\n'
        '- ask for a string,\n'
        '- ask für a boolean value,\n'
        '- create multiple choice questions or\n'
        '- create multiple choice questions with one correct answer.\n'
        'If you want to create a new quiz, call /create. 🤓\n'
        'If you want to attempt a quiz, call /attempt. 🤔\n'
        'If you want to rename one of your quizzes, call /rename. ✏️\n'
        'If you want to delete one of your quizzes, call /remove.\n\n'
        'Have fun! 🥳'
    )


def error(update, conTEXT):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, conTEXT.error)


def setup_bot(application:Application):
    """Setups the handlers"""
    # dispatch = updater.dispatcher

    # Conversation if the user wants to create a quiz
    create_states = {
        'ENTER_TYPE': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_type)],
        'ENTER_QUESTION': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_question)],
        'ENTER_ANSWER': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_answer)],
        'ENTER_POSSIBLE_ANSWER': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_possible_answer)],
        'ENTER_RANDOMNESS_QUESTION': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_randomness_question)],
        'ENTER_RANDOMNESS_QUIZ': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_randomness_quiz)],
        'ENTER_RESULT_AFTER_QUESTION': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_result_after_question)],
        'ENTER_RESULT_AFTER_QUIZ': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_result_after_quiz)],
        'ENTER_QUIZ_NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, createQuiz.enter_quiz_name)],
    }
    create_handler = ConversationHandler(
        entry_points=[CommandHandler('create', createQuiz.start)],
        states=create_states,
        fallbacks=[CommandHandler('cancelCreate', createQuiz.cancel)]
    )
    application.add_handler(create_handler)

    # Conversation if the user wants to attempt a quiz
    attempt_states = {
        'ENTER_QUIZ': [MessageHandler(filters.TEXT & ~filters.COMMAND, attemptQuiz.enter_quiz)],
        'ENTER_ANSWER': [MessageHandler(filters.TEXT & ~filters.COMMAND, attemptQuiz.enter_answer)]
    }
    attempt_handler = ConversationHandler(
        entry_points=[CommandHandler('attempt', attemptQuiz.start)],
        states=attempt_states,
        fallbacks=[CommandHandler('cancelAttempt', attemptQuiz.cancel)]
    )
    application.add_handler(attempt_handler)

    # Conversation about remove or renaming exisiting quiz
    edit_states = {
        'ENTER_NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, editQuiz.enter_name_remove)],
        'ENTER_OLD_NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, editQuiz.enter_old_name)],
        'ENTER_NEW_NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, editQuiz.enter_new_name)]
    }
    edit_handler = ConversationHandler(
        entry_points=[CommandHandler('rename', editQuiz.start_rename), CommandHandler(
            'remove', editQuiz.start_remove)],
        states=edit_states,
        fallbacks=[CommandHandler('cancelEdit', editQuiz.cancel_edit)]
    )
    application.add_handler(edit_handler)

    # help command
    application.add_handler(CommandHandler("help", print_help))

    # log all errors
    application.add_error_handler(error)


if __name__ == '__main__':
    # TODO Start message

    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    WEBHOOK = os.environ['WEBHOOK']

    # updater = Updater(TELEGRAM_TOKEN, use_conTEXT=True)

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    setup_bot(application)

application.run_webhook(
    listen="0.0.0.0",
    port=int(PORT),
    url_path=TELEGRAM_TOKEN,
    webhook_url=WEBHOOK + TELEGRAM_TOKEN
)

application.idle()

    # Start the Bot
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TELEGRAM_TOKEN)
    # updater.bot.setWebhook(WEBHOOK + TELEGRAM_TOKEN)
    # updater.idle()
