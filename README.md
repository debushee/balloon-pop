# balloon-pop  
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
