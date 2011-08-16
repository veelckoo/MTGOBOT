NOTICE: if you click start.bat and a black box flashes and disappears and nothing else happens, then you probably have to edit start.bat and make sure the path of Sikuli matches the one on your system.

Step1: find your MTGO Bot folder
Step2: rightlick on start.bat and "edit"
step3: edit the filepath to match the one on your system
step4: go to the /pricelist folder and edit the packs.txt and cards.txt file to create your pricelist
step5: right click and edit the ini.py file in the root directory of the app, and read through settings carefully and set them

*****************
Latest News:*****
*****************

This Magic Online Trading Bot was created  by Raymond Cheung.  I can be contacted at darkray16@yahoo.com.

My username on Magic Online is darkray16 .  If you're online and see me on, send me a a challenge, I play all formats and would enjoy playing with a follow Github member.

Currently, I am adding support for plugins.  The method through which I am doing this is taken from Django's Signal class and signal structure.  It's similar to event hooking in Wordpress.  A full guide will come later when I have the signaling system fully working.
Hopefully this will lead to others being able to develop plugins for the bot.

I have added support for using MySQL database for your inventory information instead of just text files.  A guide/instructions will come soon.

***************
Message: ******
***************
Despite the upcoming interface update, I WILL be continuing work on the bot.  I have finished the automated trading behavior(buying and selling) and will be shifting focus to more peripheral functions, like managing customer credits, web crawling websites for pricelists, etc.

I have finished all the core functions for the bot.  It will buy and sell cards and packs.  It will buy cards in bulk(pay certain price for all cards of certain rarity) or searching for cards and buying according to pricelist.  Although I have said I've finished the core functions, this is app is in beta so I will be continuing to fix bugs, and fine tune it to make trades faster.

The only thing missing is just to add some png images for the name of cards I have missed.  It's a time consuming task.  If you want to help me out, check out the MTGO BOT/Images/product/cards/text/preconfirm or MTGO BOT/Images/product/cards/text/confirm for examples.  All that must be done is just to take a screenshot of the name of the card, and crop it down.  Some cards look different in the pre confirm window than they do in the final confirm because they are made smaller to fit the window.

I am going to be working on developing a module for the bot that I was planning to anyways.  It is a web crawler that I plan to use to data mine all the popular websites for prices(mtgotraders.com, cardshark.com, etc) and storing the price information in a file that the bot can use to make it's pricelist.  With this, the bot could have a pricelist that would be updated hourly.



***************
Disclaimer:****
***************
I am a new programmer who is still studying much.  If you find some places in the app which I can improve, please send me an email.  It would be greatly appreciated.
I make no claims or guarantees about my bot and you use it at your own risk.


*********************
Video Tutorials:*****
*********************
You can see a demonstration of the bot at: http://www.youtube.com/watch?v=wQadgKVrGYs

I have added a video to youtube which will show you how to add cards/packs to your image folder.  This will be needed in case the bot shows an error that it cannot find a png file/image file for a product.
You can find the video here: http://www.youtube.com/watch?v=LyPO4XBFVBU


******************
Requirements:*****
******************
Sikuli
Sikuli is a graphical user scripting language which uses Python syntax.  You can download this at http://sikuli.org and there you can read about the wonderful language.  I chose Sikuli to script in, instead of AutoIt because at the time I wanted to learn Python, and since Sikuli uses Python syntax, it was perfect.  

The only major flaws I have found so far are that it cannot do a pixel scan of a .png that is completely black(#000000).  This is something I have worked around, but it does slow down the trade interactions by about 2-3 seconds total for each interaction.  The second flaw is that there are occasional glitches in the pixel scanning.  I'm still not sure what causes them, but they occur less than 2% of the time.  In the last 4 months of programming I've done on this bot, I've only ever seen it happen twice.

JRE
You will also need to download the Java Runtime Environment from http://www.oracle.com/technetwork/java/javase/downloads/index.html .  Click on the button that says "download JRE".

Magic Online
Obviously.


******************************
Starting the application:*****
******************************

I would recommend taking a look at ini.py in the MTGO BOT root folder.  It contains most of the settings required for the bot.  If there is any confusion about any of the settings, please let me know so I can rewrite the descriptions clearer.

Right click on start.bat and edit it.  Replace the "c:/program files (x86)/sikuli x/sikuli-IDE.bat" with wherever your sikuli-IDE.bat file is located.  Obvious places would be, if not in program files (x86), then in program files folder.

*IMPORTANT
I have screencapture all the images while the Magic Online App was in it's default size.  What this means is that you should not maximize the Magic Online or change it's size.  I plan to add support for a maximized window in the future.

You should already be logged in to Magic Online.  As soon as you are logged in, just start the bot and it will respond to a trade request.
For testing purposes I have have turned off signin feature.  This is so the user doesn't need to exit Magic Online everytime they have to restart the bot.

After a successful transaction, the bot will write to the /transaction_records/transactions.txt file.  It will enter in information on the transaction like what products are sold/bought, and the username of the customer.  

I have created a convenient start.bat for those who are not especially experienced in programming.  This file will start the Sikuli application, and all you have to do to start the application is click "Run".


***************
Structure:*****
***************
I have decide to use an MVC structure for my bot.  This may or may not have been the best design pattern, but it is the one I'm most familiar with.  
The view folder contains all the class definitions for interaction with the application itself.  This includes typing or reading messages from chat, posting ads in classifieds, trading, signing in, and so on.  These classes may or may not change heavily when Magic Online Version 4 rolls around.  If possible I will rewrite the application to update it for version 4.
The model folder contains all classes that deal with storing or retrieving database information, like prices, images for pixel scans, transaction records, etc.
The controller folder contains the MainController, which will coordinate the entire application.

In the main folder you will find the main app file, "bot.sikuli".  It instantiates the controller and starts everything.


**********************
Planned Features:*****
**********************
I am planning plugin support for my bot through event hooking/signals.  What this means is you can customize features of the bot to suit your own needs.  Once I'm closer to completion I will release more information about the full scope of customizability and a guide.