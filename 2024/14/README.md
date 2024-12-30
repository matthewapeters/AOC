# NOTES ON DAY 14 - Part 2

## SPOILER ALERT

**I give my solution below**

After researching the problem, I understand there is a method called the Chinese Remainder Theory (CRT)
that can be used to identify the number of moves (seconds) that will align the X and Y offsets, providing
the Chrsitmas tree image.

Unfortunately, I could not find libraries or satisfactory implementation details for me to provide my own working
solution - so I punted.  I modified aoc_14_2 so that it accepts keyboard input at run-time.

To run the app:

aoc_14_2 <name prefix of input and floor file> <moves to make before interaction>

```sh
./aoc_14_2 sample 22
```

Keyboard:

Right Arrow: move forward 1 second
Left Arrow: Rewind 1 second
Up Arrow: Move forward as many seconds as the horizontal width of the floor

The up arrow effectively modulates the robots in the Y dimension of their vector,
but retains their X vector.

At 22 seconds in, I observed vertical structure in the image:

```

# structure observed on these columns:  |                             |
#                                       V                             V
# (partial screen scrape)

        @                               @                                                            
                                               @ @                  @                                
       @                                     @                                @                      
      @                                 @  @            @  @       @  @                              
                                          @            @ @            @                              
 @                                 @    @               @ @@@                                        
                               @                     @   @       @                                   
                                                 @           @                                       
                                                 @    @      @ @                                     
                   @                    @                       @                                    
                             @          @@    @                       @      @                       
                                        @                     @     @                                
                                                 @@                                                  
                                          @           @  @   @                                       
                                                                 @                                   
                                    @              @                          @                      
                                  @     @        @          @  @@                                    
                                                @         @       @                                  
     @      @                               @    @    @          @                                   
                                        @           @      @    @                                    
                @                                     @@     @    @   @                              
                                                        @  @          @                              
                                        @            @  @@      @                 @  @               
                   @                 @               @                                               
                    @                               @ @          @                           @       
                                                         @    @                                @     
            @                                        @ @@             @                              
                                                              @                                      
              @                         @          @   @@             @                              
                                                  @       @    @                                     
                                                   @@   @@  @                                      @ 
                 @                                     @  @                                          
                                   @    @                   @                                        
                         @                    @ @  @@@@  @                                           
@                                                 @  @                                               
  @                    @                    @  @  @   @  @  @    @                                   
                                                    @ @                          @                   
                                               @@@    @               @                              
              @           @             @           @         @       @                   @        @ 
                                   @         @    @    @@@ @ @        @                              
@           @                           @                                                            
                                                                      @                              
                            @  @                  @ @ @        @                                     
                                        @             @                    @                         
                                    @   @       @  @    @            @@            @                 
                                                     @    @                                          

```

By then paging up, I find a frame with the Christmas tree:

```sh
MOVES:  6587
                                                                                  @                @ 
                                                                                                     
                              @            @                                                         
 @     @                                     @                                                       
           @                     @ @                                                                 
                                             @  @                            @                      @
                                                                                                     
                                                    @                                                
            @                     @                                                                  
                                                                                                     
                                                                  @                                  
                                                @        @                    @                      
              @        @             @                                       @                       
                                                                                                     
     @       @                                                            @                          
                       @                                                                             
                                                          @                                          
 @                                                                                                   
                                                                                                     
                                                           @                                         
                                    @                                             @                  
                   @                                                                                 
@               @     @        @                                                           @  @      
                                                                                                     
  @                                                              @                           @  @    
                   @                                                                                 
                                                                                                     
        @                                              @                                       @     
                                                                                                     
                                                                                                     
                                                     @                @         @                    
           @                     @       @                                                           
@                                                                                                    
             @                          @        @                                                   
                  @                       @                                                          
                  @                                                                                  
                                              @                                                      
                                                                @                                    
                                                      @                                              
                                                                                                     
                                                    @                                       @        
   @                     @               @                @                                          
                                                                                            @        
                                   @                                       @                         
                                    @                                                                
                           @                                                                         
                                                                                                     
                                 @      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                              
            @                           @                             @                              
                                        @                             @          @                   
                                        @                             @                              
                    @                   @                             @                              
                                        @              @              @                              
                                        @             @@@             @                   @          
                                        @            @@@@@            @                              
                                      @ @           @@@@@@@           @                              
                                        @          @@@@@@@@@          @                              
                                        @            @@@@@            @                              
             @                          @           @@@@@@@           @           @         @        
     @  @                               @          @@@@@@@@@          @     @                        
       @        @                       @         @@@@@@@@@@@         @                              
                                        @        @@@@@@@@@@@@@        @                              
 @   @                                  @          @@@@@@@@@          @                              
                                        @         @@@@@@@@@@@         @       @                      
                 @                      @        @@@@@@@@@@@@@        @                              
      @                      @          @       @@@@@@@@@@@@@@@       @                              
@                                       @      @@@@@@@@@@@@@@@@@      @                              
                                        @        @@@@@@@@@@@@@        @    @                         
     @                                  @       @@@@@@@@@@@@@@@       @                              
                                        @      @@@@@@@@@@@@@@@@@      @                              
                                        @     @@@@@@@@@@@@@@@@@@@     @                              
                 @                      @    @@@@@@@@@@@@@@@@@@@@@    @                   @          
                                        @             @@@             @                              
              @                         @             @@@             @                              
                                        @             @@@             @            @                 
                                        @                             @                              
                                        @                             @                              
                                        @                             @   @                          
                                        @                             @            @                 
                                        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                              
                           @                                                                         
            @                                                                                        
                                                                  @                                  
                              @                                                    @                 
                                                    @                                                
                                   @                                                                 
                                                            @                                        
                            @       @                                                                
                                                       @                                             
                          @ @                                                @                 @     
          @                                         @            @                                   
                                                           @                          @              
                   @      @                                                                          
     @                         @                                @@                                   
                      @                                        @                                   @ 
                                       @       @                                     @               
                                                                      @                 @            
                                                                        @                            
                                                                                                     
          @                                                       @                                  
            @                @                                                       @               
              @       @                                                                              


```
