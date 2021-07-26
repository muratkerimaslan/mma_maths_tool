# mma_maths_tool
Web crawler starting from a wikipedia page of an mma fighter and branching out using clickable links from the page

"MMA maths" is the idea that fighter A won against fighter B, and fighter B won against fighter C, so fighter A should also win against fighter C. This obviously doesn't make much sense as if we applied this reasoning to rock-paper-scissors, we could find that rock beats paper.

This program is written to find how many fighters Jake Paul could beat if "MMA maths" logic was taken to the extreme. It turns out if we keep on going deeper, we could reach almost every fighter (the web crawler would reach them using BFS) and conclude that Jake Paul could beat them because jake Paul beat ben askren and ben askren beat someone and so on and on and on. The crawler starting from Ben Askren's wikipedia page clicked on 2526 pages of MMA fighter wikipedia pages (using BFS starting from Ben Askren wikipedia page), and saw more than 16000 unique names, fighters ranging from heavyweight to the strawweight. 
