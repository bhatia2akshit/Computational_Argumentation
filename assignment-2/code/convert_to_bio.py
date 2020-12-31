import argparse
import glob
import re
import json
import os
import itertools

from nltk import word_tokenize

def modify_label_spans(char_map, labels_spans, essay_text, essay_new_text):

    new_label_spans = []

    for a_label in labels_spans:
        label_text  = a_label['text']
        label_start = a_label['span'][0]
        label_end   = a_label['span'][1]

        if label_text == '': #labels file sometime ends with extra newline
            continue
        
        if int(label_end) > len(essay_text):
            print('out of boundary case...')
            label_end = len(essay_text)

        start = char_map[label_start]
        end   = char_map[label_end]

        new_span  = essay_new_text[start:end]
        old_span  = essay_text[label_start:label_end]
        
        print('old span:  ', old_span)
        print('new span:  ', new_span)

        #check if the last character consists of new line and if so then shorten the boundary
        if new_span[-1] == '\n':
            end= end - 1

        if new_span[-1] == ' ':
            end= end - 1


        if end+1 < len(essay_new_text) and essay_new_text[end+1] != ' ' and essay_new_text[end+1] != '\n':
            new_end = end
            while essay_new_text[new_end] != ' ' and essay_new_text[new_end] != '\n':
                new_end = new_end+1

            end = new_end

        if essay_new_text[start-1] != ' ' and essay_new_text[start-1] != '\n':
            new_start = start-1
            while essay_new_text[new_start] != ' ' and essay_new_text[new_start] != '\n':
                new_start = new_start -1

            start = new_start+1

        new_label_spans.append({'text': label_text, 'span': [start, end]})

    return new_label_spans

def tokenize_essay(essay):

    essay_text = essay['text']

    #Do some conversions
    matches = re.finditer('‘(\w*)’', essay_text)
    for i in matches:
        essay_text = essay_text.replace(i.group(0), '“' + i.group(1) + '”')

    essay_text = essay_text.replace('’', '\'')
    essay_text = essay_text.replace('`', '\'')
    essay_text = essay_text.replace('“', '"')
    essay_text = essay_text.replace('”', '"')
    essay_text = essay_text.replace('\'\'', '"')

    essay_text = '\n'.join([line.strip() for line in essay_text.split('\n')])
    essay_text = essay_text.replace('\n\n', '\n')
    #End of conversions...

    #construct the new text
    essay_lines    = re.split("(\n)", essay_text)
    essay_new_text = ''.join([' '.join(word_tokenize(line)) if line != '\n' else line for line in essay_lines])
    
    #reset the double quotes
    essay_new_text = essay_new_text.replace('``', '"').replace('\'\'', '"')

    #create a map between chars from old text to new text
    char_map  = {}
    a_old_chr_idx = 0
    a_new_chr_idx = 0
    while a_old_chr_idx < len(essay_text):
        while a_new_chr_idx < len(essay_new_text) and essay_new_text[a_new_chr_idx] != essay_text[a_old_chr_idx]:
            # print(a_new_chr_idx, essay_new_text[0:a_new_chr_idx])
            # print('=========')
            # print(a_old_chr_idx, essay_text[0:a_old_chr_idx])

            a_new_chr_idx+=1

        char_map[a_old_chr_idx] = a_new_chr_idx
        a_old_chr_idx+=1

    char_map[len(essay_text)] = len(essay_new_text)

    #construct new boundaries for labels
    essay['text'] = essay_new_text
    essay['premises'] = modify_label_spans(char_map, essay['premises'], essay_text, essay_new_text)
    essay['claims'] = modify_label_spans(char_map, essay['claims'], essay_text, essay_new_text)
    essay['major_claim'] = modify_label_spans(char_map, essay['major_claim'], essay_text, essay_new_text)

    return essay

def attach_labels(tokens, label_spans, class_name):
    ch_idx = 0
    updated_tokens = []

    for token_and_label in tokens:
        token, label = token_and_label[0], token_and_label[1]

        if token == '__END_PARAGRAPH__':
            updated_tokens.append(('__END_PARAGRAPH__', 'O'))
            continue

        for label_span in label_spans:
            label_start, label_end = label_span['span'][0], label_span['span'][1]
            if ch_idx >= int(label_start) and (ch_idx + len(token)) <= int(label_end):
                label = 'B-'+class_name if ch_idx == int(label_start) else 'I-'+class_name

        updated_tokens.append((token, label))
        ch_idx+= (len(token) + 1)

    return updated_tokens

def to_bio(essay_item):
    essay_text = essay_item['text']

    essay_lines  = [x.split(' ') + ['__END_PARAGRAPH__'] if x != '\n' else ['\n', '__END_PARAGRAPH__'] for x in essay_text.split('\n')]
    essay_tokens = list(itertools.chain.from_iterable(essay_lines))
    #essay_tokens = word_tokenize(essay_text)

    #add default label for all tokens
    tokens_and_labels = [(x, 'O') for x in essay_tokens]
    
    tokens_and_labels = attach_labels(tokens_and_labels, essay_item['premises'], 'PREMISE')
    tokens_and_labels = attach_labels(tokens_and_labels, essay_item['major_claim'], 'MAJOR-CLAIM')
    tokens_and_labels = attach_labels(tokens_and_labels, essay_item['claims'], 'CLAIM')

    return '\n'.join(['\t'.join(x) for x in tokens_and_labels])


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--output_path', type=str)


    args = parser.parse_args()

    json_corpus = json.load(open(args.data_path))

    bio_output = ''
    for essay in json_corpus:
        essay = tokenize_essay(essay)
        bio_tokens = to_bio(essay)
        print(bio_tokens)
        bio_output += bio_tokens + '\n__END_ESSAY__\n'

    with open(args.output_path, 'w') as file:
        file.write(''.join(bio_output))