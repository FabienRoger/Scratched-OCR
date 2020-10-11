int size = 32;
int strength = 5;


String[] fontList = PFont.list();

int[] wrongs = {2, 13, 15, 16, 20, 70, 79, 450, 360, 362, 481,482,483,479, 264, 267, 269, 276,
                9, 8, 12, 108, 171, 176, 214, 231, 334, 335, 379, 378, 380, 382, 396, 420, 448,
                134, 221};
String characters = "abcdefghijklmnopqrstuvwxyz";

void setup(){
  size(1600, 600);
  //displayAll();
  //createImg("W",50,"test.png");
  //createDataSet(1000);
  //createFullDataSet();
  createDualDataSet();
}

boolean contains(int[] l, int x){
  for(int y:l){
    if(x==y)return true;
  }
  return false;
}

void displayAll(){
  printArray(fontList);
  background(255);
  
  fill(0);
  for(int i = 0;i<fontList.length;i++){
    textFont(createFont(fontList[i],25));
    if(!contains(wrongs,i)){
    text("a",(i%50)*20,50*(1+i/50));
    }else{
      ellipse((i%50)*20,50*(1+i/50),5,5);
    }
  }
}

void createImg(String s, int fontN, String saveFile, boolean damaging){
  PGraphics pg = createGraphics(size,size);
  pg.beginDraw();
  pg.background(255);
  pg.fill(0);
  pg.textFont(createFont(fontList[fontN],28));
  pg.text(s,2,22);
  if(damaging)
    damage(pg);
  pg.endDraw();
  image(pg,0,0);
  pg.save(saveFile);
}

void createDataSet(int size, boolean damaging){
  for(int i = 0;i<size;i++){
    if((i%100)==0)println(i);
    int fontN = floor(random(fontList.length));
    while(contains(wrongs, fontN))fontN = floor(random(fontList.length));
    String c = str(characters.charAt(floor(random(characters.length()))));
    String saveFile = "data/"+c+"/img"+str(i)+".png";
    createImg(c, fontN, saveFile, damaging);
    
  }
  println("done");
}

void createFullDataSet(){
  for(int i = 0;i<fontList.length;i++){
    if((i%10)==0)println(i);
    if(!contains(wrongs, i)){
      String set = "train";
      float r = random(1);
      if(r<0.1){
        set = "test";
      }else if(r<0.2){
        set = "val";
      }
      for(int j = 0;j<26;j++){
        int fontN = i;
        String c = str(characters.charAt(j));
        String saveFile = "data/"+set+"/"+c+"/img"+str(i)+".png";
        createImg(c, fontN, saveFile, true);
      }
    }
  }
  println("done");
}

void createDualDataSet(){
  for(int i = 0;i<fontList.length;i++){
    if((i%10)==0)println(i);
    if(!contains(wrongs, i)){
      String set = "train";
      float r = random(1);
      if(r<0.1){
        set = "test";
      }else if(r<0.2){
        set = "val";
      }
      for(int j = 0;j<26;j++){
        int fontN = i;
        String c = str(characters.charAt(j));
        String saveFileOrigin = "data/origin"+set+"/"+c+"/img"+str(i)+".png";
        String saveFileDamaged = "data/damaged"+set+"/"+c+"/img"+str(i)+".png";
        createImg(c, fontN, saveFileDamaged, true);
        createImg(c, fontN, saveFileOrigin, false);
      }
    }
  }
  println("done");
}

void damage(PGraphics pg){
  
  strokeWeight(1);
  for(int i = 0;i<strength;i++){
    stroke(random(100));
    pg.line(random(size),random(size),random(size),random(size));
  }
}