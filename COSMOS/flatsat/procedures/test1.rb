require 'csv'
load 'PS_DP811A.rb'
file = CSV.open('test.csv','w')
file << [1,2,3,4,5]
file << [6,7,8,9,10]