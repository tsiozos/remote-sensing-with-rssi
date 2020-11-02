#calc transmit probabilities
# PROBLEM: a radio system with nodes A,B transmits
# n number of packets from A to B. What is the probability
# at least on packet to travel successfully from A to B?
# ANSWER: the success rate is the one calculated
# y: probability of at least one packet success
# p: probability of packet loss (B doesn't receive one packet)
# n: number of tries the packet is send from A to B
1;
# calculate the success rate probability given p loss prob
# and n number of tries
# p: packet loss probability
# n: number of tries
function y = successR (p, n)
  y = 1-p.^n;
endfunction

#calculate how many tries are needed with loss prob p
# PROBLEM: if packet loss is p and we need a success rate
# of y, how many packets do we need to send?
# ANSWER: the packets should be equal or more than that.
# to reach success rate y
# y: success rate probability [0-1]
# p: packet loss probability [0-1]
function n = triesN(y,p)
  n = ceil(log(1-y)./log(p));
endfunction

#calculate the packet loss probability given 
# PROBLEM: how much should the packet loss prob be if
# we want to have a success rate y with n tries?
# the success rate you want and the number of tries you want
# ANSWER the packet loss must be LESS than that
# n: the number of tries
# y: success rate probability
function p = lossP(y,n)
  p = (1-y).^(1./n);
endfunction


# given RSSI how many tries do we need so we
# will have a success rate of y?
# rssi: the measured rssi btw sender/receiver
#    y: the success rate probability we need
function t = triesFromRSSI(rssi,y,maxtries = 10)
  rssi2 = rssi + 100
  p = min([1,5936.2673.*rssi2.^(-3.7231)])
  if (p==1)
    t = maxtries
  else
    t = max([1,triesN(y,p)])  #if tries fall below 1, at least 1 try
  endif
#  t = min([maxtries,t])
endfunction
