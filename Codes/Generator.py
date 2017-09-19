# Author - Rajdeep Pinge
# Date - 18th April, 2017

# The following link has been referred when writing this code: https://github.com/CMasanto/melody-generator 

# Code to generate music by storing an existing song in the form of a markov chain


from midiutil.MidiFile import MIDIFile

import random

def getNoteList(fp):
	noteLst = []

	for line in fp:
		line = line.rstrip('\n')

		if line[:1] != "#" and line[:1] != "":
			if int(line) != -1:
				noteLst.append(int(line))

	return noteLst


def addNewNote(lastNote, last2Note, last3Note, markov_chain_3rd_order, markov_chain_2nd_order, markov_chain_1st_order):
	if (last3Note, last2Note, lastNote) in markov_chain_3rd_order.keys():
		return random.choice(markov_chain_3rd_order[(last3Note,last2Note,lastNote)])
	elif (last2Note, lastNote) in markov_chain_2nd_order.keys():
		return random.choice(markov_chain_2nd_order[(last2Note,lastNote)])
	else:
		return random.choice(markov_chain_1st_order[lastNote])


def generateNewSongNoteList(noteLst, markov_chain_3rd_order, markov_chain_2nd_order, markov_chain_1st_order):

	lastNote = random.choice(noteLst)
	last2Note = random.choice(noteLst)
	last3Note = random.choice(noteLst)

	songNoteLst = []

	for newNoteIndex in range(50):
		currNote = addNewNote(lastNote, last2Note, last3Note, markov_chain_3rd_order, markov_chain_2nd_order, markov_chain_1st_order)
		songNoteLst.append(currNote)
		last3Note = last2Note
		last2Note = lastNote
		lastNote = currNote

	return songNoteLst


def createFirstOrderMarkovChain(noteLst):
	print("Creating 1st order markov chain")
	markov_chain_1st_order = {}
	for i in range(len(noteLst)-1):
		if noteLst[i] not in markov_chain_1st_order.keys():
			markov_chain_1st_order[noteLst[i]] = []

		markov_chain_1st_order[noteLst[i]].append(noteLst[i+1])

	return markov_chain_1st_order

def createSecondOrderMarkovChain(noteLst):
	print("Creating 2nd order markov chain")
	markov_chain_2nd_order = {}
	for i in range(len(noteLst)-2):
		if (noteLst[i],noteLst[i+1]) not in markov_chain_2nd_order.keys():
			markov_chain_2nd_order[(noteLst[i],noteLst[i+1])] = []

		markov_chain_2nd_order[(noteLst[i],noteLst[i+1])].append(noteLst[i+2])

	return markov_chain_2nd_order

def createThirdOrderMarkovChain(noteLst):
	print("Creating 3rd order markov chain")
	markov_chain_3rd_order = {}
	for i in range(len(noteLst)-3):
		if (noteLst[i],noteLst[i+1],noteLst[i+2]) not in markov_chain_3rd_order.keys():
			markov_chain_3rd_order[(noteLst[i],noteLst[i+1],noteLst[i+2])] = []

		markov_chain_3rd_order[(noteLst[i],noteLst[i+1],noteLst[i+2])].append(noteLst[i+3])

	return markov_chain_3rd_order


def generateNewSongNoteList_1st_order(noteLst, markov_chain_1st_order):

	print("Generating Song Notes")

	lastNote = random.choice(noteLst)
	songNoteLst = []
	for newNoteIndex in range(50):
		currNote = random.choice(markov_chain_1st_order[lastNote])
		songNoteLst.append(currNote)
		lastNote = currNote

	return songNoteLst


def generateNewSongNoteList_2nd_order(noteLst, markov_chain_2nd_order):

	print("Generating Song Notes")

	lastNote = 68
	last2Note = 69
	songNoteLst = []
	for newNoteIndex in range(50):
		currNote = random.choice(markov_chain_2nd_order[(last2Note,lastNote)])
		songNoteLst.append(currNote)
		last2Note = lastNote
		lastNote = currNote

	return songNoteLst


def generateNewSongNoteList_3rd_order(noteLst, markov_chain_3rd_order):

	print("Generating Song Notes")

	lastNote = 64
	last2Note = 68
	last3Note = 69
	songNoteLst = []
	for newNoteIndex in range(50):
		currNote = random.choice(markov_chain_3rd_order[(last3Note,last2Note,lastNote)])
		songNoteLst.append(currNote)
		last3Note = last2Note
		last2Note = lastNote
		lastNote = currNote

	return songNoteLst


def generateMidiFile(songNoteLst, MCType):
	print("Generating Song File")

	newSong = MIDIFile(1)

	# Tracks are numbered from zero. Times are measured in beats.
	track = 0   
	time = 0

	# Add track name and tempo.
	newSong.addTrackName(track, time, "Song Generated Using Markov Chain")
	newSong.addTempo(track, time, 360)

	channel = 0

	for note in songNoteLst:
		if note != -1:		
			# Add a note. addNote expects the following information:

			pitch = note
			duration = random.randint(1,4)
			volume = 255

			# Now add the note.
			newSong.addNote(track,channel,pitch,time,duration,volume)
			time += duration


	# And write it to disk.
	write_file_name = "output_" + MCType + "_MC.midi"
	binfile = open(write_file_name, 'wb')
	newSong.writeFile(binfile)
	binfile.close()

	print("Finished")



def print_as_matrix(markov_chain, limit=10):
    columns = []
    for from_note, to_notes in markov_chain.items():
        for note in to_notes:
            if note not in columns:
                columns.append(note)

    _col = lambda string: '{:<14}'.format(string)
    _note = lambda string: '{:<14}'.format(string)
    out = _col('')
    out += ''.join([_col(_note(note)) for note in columns[:limit]]) + '\n'

    for from_note, to_notes in markov_chain.items():
        out += _col(from_note)

        for note in columns[:limit]:
        	count = 0
        	for val in markov_chain[from_note]:
        		if note == val:
        			count += 1

        	out += _col(count)
        out += '\n'
    print(out)

######################################## Testing part ####################################################

file_path = "Corpus/MichaelJacksonNotes.txt"
fp = open(file_path, 'r')

noteLst = getNoteList(fp)

markov_chain_1st_order = createFirstOrderMarkovChain(noteLst)
print_as_matrix(markov_chain_1st_order)

markov_chain_2nd_order = createSecondOrderMarkovChain(noteLst)
print_as_matrix(markov_chain_2nd_order)

markov_chain_3rd_order = createThirdOrderMarkovChain(noteLst)
print_as_matrix(markov_chain_3rd_order)



songNoteLst = generateNewSongNoteList_1st_order(noteLst, markov_chain_1st_order)
MCType = "1st_order"
generateMidiFile(songNoteLst, MCType)

songNoteLst = generateNewSongNoteList_2nd_order(noteLst, markov_chain_2nd_order)
MCType = "2nd_order"
generateMidiFile(songNoteLst, MCType)

songNoteLst = generateNewSongNoteList_3rd_order(noteLst, markov_chain_3rd_order)
MCType = "3rd_order"
generateMidiFile(songNoteLst, MCType)

songNoteLst = generateNewSongNoteList(noteLst, markov_chain_3rd_order, markov_chain_2nd_order, markov_chain_1st_order)
MCType = "Combined"
generateMidiFile(songNoteLst, MCType)
