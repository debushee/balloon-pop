# balloon-pop  
This game requires a decent graphics card, a decent sized monitor (greater than 24 inch) and a webcam (ideally external).  
The game starts by asking the user to enter their name and then click on Play to start the game.  
Balloons float up from the bottom to the top of the screen and the player uses one hand (it works better if you hide the other hand from the camera)  
to pop the balloons on the screen.  The more balloons you pop, the more points you get but also the faster the balloons float up the screen.  Good luck!

On Windows 10 machine  
In VS Code use the command terminal for this (not Powershell):  
python3 -m venv venv .\venv\Scripts\activate  

On a Mac activate with this:  
source venv/bin/activate  

Then for Mac and Win:  
pip3 install -r requirements.txt   
(If require access GCP Firestore connectivity....)  
pip3 install google-cloud-firestore  
pip install --upgrade google-cloud-datastore  

Now you are ready to run the game: 
cd back to the main directory and then run:  
python BalloonPop.py
