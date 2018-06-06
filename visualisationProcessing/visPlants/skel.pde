class Plants
{
  ArrayList<Skeleton> skel = new ArrayList<Skeleton>(); 
  int tMax;
  int tTrail;
  float scale;
  ArrayList<Float> xTrail = new ArrayList<Float>(); 
  ArrayList<Float> zTrail = new ArrayList<Float>(); 
  Plants(int tTrail0)
  {
    scale=300;
    tTrail = tTrail0;
  }

  void updateFile(String file)
  {
    
    Table table = loadTable(file);

    tMax = table.getRowCount()/NElements;
    for (int k = 0; k<tMax; k++)
    {
      skel.add(new Skeleton(scale));
      for (int j=0; j<NElements; j++)
      {
        TableRow row = table.getRow(k*NElements + j);
        skel.get(skel.size()-1).updateValues(j, row.getFloat(0), row.getFloat(1), row.getFloat(2));
      }
      
    }
  }

  void draw(int frame)
  {
    if (frame == 0)
    {
      xTrail.clear();
      zTrail.clear();
    }
    xTrail.add(skel.get(frame).x[NElements-1]);
    zTrail.add(skel.get(frame).z[NElements-1]);
    if (xTrail.size()>tTrail)
    {
      xTrail.remove(0);
      zTrail.remove(0);
    }
    //stroke(034,190,190,140);
    //fill(0,50);

    noStroke();
    int step=1;
    for (int j=step; j<xTrail.size(); j+=step)
    {
      fill(255,180,120,60*(float)j/(float)tTrail);
      //strokeWeight(5.0*(float)j/(float)tTrail);
      //line(xTrail.get(j-step)*scale, zTrail.get(j-step)*scale, xTrail.get(j)*scale, zTrail.get(j)*scale);
      ellipse(xTrail.get(j)*scale, zTrail.get(j)*scale,10.0*(float)j/(float)tTrail,10.0*(float)j/(float)tTrail);
    }
    
    
    skel.get(frame).draw();
  }
}

class Skeleton
{
  float[] x = new float[NElements]; 
  float[] y = new float[NElements]; 
  float[] z = new float[NElements]; 
  float scale;
  int step;
  Skeleton(float scale0)
  {
    scale = scale0;
    step = 9;
  }

  void updateValues(int idx, float x0, float y0, float z0)
  {
    x[idx] = x0;
    y[idx] = y0;
    z[idx] = z0;
  }

  void draw()
  {
    stroke(0,10);
    strokeWeight(4);
    
    for (int j=step; j<NElements; j+=step)
    {
      line(x[j-step]*scale, z[j-step]*scale, x[j]*scale, z[j]*scale);
    }
    noStroke();
    fill(255,200,220,200);
    ellipse(x[NElements-1]*scale,z[NElements-1]*scale,10,10);
  }
}
