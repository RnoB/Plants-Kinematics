
int fading;
String path = "C:/Users/renaud/Documents/Plants-Kinematics/data/855a256a-e5d7-4168-b6d9-a7a340606d97/";
ArrayList<Plants> plants = new ArrayList<Plants>(); 
int NElements = 1000;
int frame;
int frameMax;
int nPlants;
int tTrailMax;
float scale0;
boolean grabImages;

void setup()
{
  grabImages = true;
  colorMode(HSB);
  size(1080, 1080);
  background(255);
  smooth(8);
  scale0=318;
  if(!grabImages)
  {
    //frameRate(12);
  }
  fading = 255;
  tTrailMax=30;

  File[] files = listFiles(path, "extension=csv");
  //print(files.length);
  for (int k = 0; k<files.length; k++)
  {
    plants.add(new Plants(tTrailMax,scale0));
    plants.get(plants.size()-1).updateFile(path+files[k].getName());
  }
  frameMax = plants.get(plants.size()-1).tMax;
  frame=0;
  nPlants = plants.size();
}

void draw()
{
  //background(255, fading);
  noStroke();
  fill(255,fading);
  rect(0,0,width,height);
  
  for (int k = 0; k<nPlants; k++)
  {
    plants.get(k).draw(frame);
  }
  frame++;
  if (frame>frameMax-1)
  {
    if(grabImages)
    {
      exit();
    }
    else
    {
      frame =0;
    }
  }
  
  if(grabImages)
  {
    saveFrame("images-######.png");
  }
}
