# NFT-Generator
Generates NFT collections using different assets (hats glasses and so on) and combining them to create different characters


## Different Rarity Settings
using the chances.json file specify percentages for each accessory by first typing the path to the accessory file and than specifying the percentage. 
Note that all the percentages should add up to 100 in each accessory category. Heres an example:
```json
"accessories\\eye\\eye_patch.png":        60,
"accessories\\eye\\glasses_matrix.png":   35,
"accessories\\eye\\monicle.png":           5
```
Although you specify chances of different accessories in different categories you do have to specify the chance that a character will have a category in the code itself. 
For example we set the chance of eye_patch.png to be 60. but eye_patch.png counts as a hat accessory which has a 35% chance of being added. 
That Means That an eyepatch will apear 0.35 * 0.6 = 0.21 = 21% of the time.
```python
person.add_accessory('hat', 35)
```

## Usage
After specifying different rarities use the Main.py file to generate any amount of NFT-s. open a command prompt in the same directory as the Main.py file and type:
```
python Main.py N
```
where N is the number of NFT-s

## Output
After the script is done (see command line output). It will output different NFT-s in the outputs folder. 
output folder images will be in high resolution but the images in "output/raw" folder will be in original 16x16 image size.
The Script also outputs metadata for each nft in the metadata.json file and the actual amounts of accessories in % in the amounts.json file.
