python build_test_LM.py -b input.train.txt -t crossval.text.txt -o input.predict.txt
python eval.py input.predict.txt input.train.txt
