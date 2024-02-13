**Keyauth Telegram Bot**

This Telegram bot allows you to manage Keyauth licenses using simple commands. It interacts with the Keyauth API to create licenses, ban licenses, and retrieve information about licenses.

**Features**
- **Create a License:** Generate new Keyauth licenses with specified expiration and quantity.
- **Ban a License:** Prohibit the use of a license in an application by banning it.
- **Lookup a License:** Retrieve detailed information about a specific license.

**Commands**
- `/create <expiration> <quantity>`: Create a new license with the specified expiration (in days) and quantity.
- `/ban <key> <reason>`: Ban a license with the provided key, indicating a reason for the ban.
- `/lookup <key>`: Look up detailed information about a license using its key.

**Clone this repository to your local machine.**

**Install the required dependencies by running** `pip install telebot`.

**Create a file named secure.json in the project's root directory.**

**Add your Telegram bot token and your Keyauth seller key to the secure.json file in the following format:**

```json
{
    "TELEGRAM_BOT_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN_HERE",
    "sellerkey": "YOUR_SELLER_KEY_HERE"
}
```


Run the bot script by executing python bot.py.

**Usage**

Once the bot is running, you can interact with it by sending commands in any chat where the bot is added. Use the commands mentioned above to create, ban, or look up information about licenses.

License

This project is licensed under the MIT License - see the LICENSE file for more details.
