
int fading;
String path = "C:/Users/renaud/Documents/trialCsv/";
ArrayList<Plants> plants = new ArrayList<Plants>(); 
int NElements = 1000;
int frame;
int frameMax;
int nPlants;
int tTrailMax;
void setup()
{
  colorMode(HSB);
  size(1080, 512);
  background(255);
  smooth();
  frameRate(12);
  fading = 255;
  tTrailMax=30;

  File[] files = listFiles(path, "extension=csv");
  //print(files.length);
  for (int k = 0; k<files.length; k++)
  {
    plants.add(new Plants(tTrailMax));
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
    frame =0;
  }
}
