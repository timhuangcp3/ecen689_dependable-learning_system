module FIFO(Data_Out, Full, Empty, Data_In, wr_en, rd_en, clk, reset) ;

input [7:0] Data_In ;
input wr_en ;
input rd_en ;
input clk ;
input reset ;

output [7: 0] Data_Out ;
output Full ;
output Empty ;

reg [7: 0] Data_Out ;
reg [7:0] memory [9:0] ;
reg [9:0] rd_ptr, wr_ptr, depth_cnt ;

//PUSH
always @ (posedge clk)
begin
   if (reset) begin
      wr_ptr <= 'h0 ;
   end
   else begin
      if (wr_en && !Full) begin
         memory [wr_ptr] <= Data_In ;
         wr_ptr <= wr_ptr + 1 ;
      end
   end   
end

//POP
always @ (posedge clk)
begin
   if (reset) begin
      rd_ptr <= 'h0 ;
   end
   else begin
      if (rd_en && !Empty) begin
         Data_Out <= memory [rd_ptr] ;
         rd_ptr <= rd_ptr + 1 ;
      end
   end   
end

//Depth Count
always @ (posedge clk)
begin
   if (reset) begin
      depth_cnt <= 'h0 ;
   end
   else begin
      if (wr_en && !Full)
         depth_cnt <= depth_cnt + 1 ;
     else if (rd_en && !Empty)
         depth_cnt <= depth_cnt - 1 ;
      //add one more condition to check simultaneous WR & RD.
   end   
end

   assign Empty = (depth_cnt == 'h0)?1 : 0 ;
   assign Full  = (depth_cnt == 9)? 1 : 0 ;

   assert property (!(Full && Empty));
   assert property ((Full & !rd_en & !reset) |=> Full);
   assert property (Empty & !wr_en |=> Empty);


   
endmodule
