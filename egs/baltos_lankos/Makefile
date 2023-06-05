############################################
-include Makefile.options
############################################
corpus?=blankos.v01
wav_gz?=../data/blankos.tgz
prefix?=BLA
out_dir?=.data/$(corpus)
python_dir=${CURDIR}/../../data_prep
python_cmd=PYTHONPATH=../../ python
MAX_LINES?=1000000000
wav_dir=.wav

bin=$(shell pwd)/bin
############################################
SHELL=/bin/bash
.SHELLFLAGS=-o pipefail -c
############################################
${out_dir}/extracted: 
	mkdir -p $@
${out_dir}/lab: 
	mkdir -p $@
${out_dir}/range:
	mkdir -p $@
${out_dir}/wav:
	mkdir -p $@
${out_dir}/text: 
	mkdir -p $@
${out_dir}/lists:
	mkdir -p $@
$(out_dir)/$(corpus):
	mkdir -p $@
$(out_dir)/$(corpus)/wavs:
	mkdir -p $@
############################################
${out_dir}/extracted/initial.mlf: ${mlf} | ${out_dir}/extracted
	cp $^ $@
############################################
${out_dir}/extracted/utf.mlf: ${out_dir}/extracted/initial.mlf | ${out_dir}/lab
	pv $^ | head -n $(MAX_LINES) > $@
	touch $@
############################################
${out_dir}/extracted/fixed.mlf: ${out_dir}/extracted/utf.mlf | ${out_dir}/lab
	pv $^ | $(python_cmd) $(python_dir)/exclude_files.py --exclude "$(exclude)" \
		| $(python_cmd) $(python_dir)/fix_mlf.py \
		| $(python_cmd) $(python_dir)/change_name.py --prefix '$(prefix)_' > $@
############################################
${out_dir}/extracted/fixed.split.mlf: ${out_dir}/extracted/fixed.mlf ${out_dir}/range/.done
	pv ${out_dir}/extracted/fixed.mlf | $(python_cmd) $(python_dir)/mlf_by_range.py --rangeDir ${out_dir}/range > $@_
	mv $@_ $@
############################################
${out_dir}/lab/.done: ${out_dir}/extracted/fixed.mlf | ${out_dir}/lab
	pv $^ | $(python_cmd)  $(python_dir)/split_mlf.py --outDir `dirname $@`
	touch $@
############################################
${out_dir}/range/.done: ${out_dir}/lab/.done | ${out_dir}/range
	ls -1 ${out_dir}/lab/*.lab | xargs -n1 -I {} -P 4 sh -c \
		'base=`basename {} .lab`; \
		cat {} | $(python_cmd) $(python_dir)/mlf_to_range.py --maxSil 400 > ${out_dir}/range/$${base}.split.range'
	touch $@
############################################
${out_dir}/wav/split.sh: ${out_dir}/range/.done | ${out_dir}/wav
	rm -f $@_
	ls -1 ${out_dir}/range/*.range | xargs -n1 -I {} sh -c \
		'base=`basename {} .split.range`; \
		cat {} | $(python_cmd) $(python_dir)/range_to_split_sh.py --name $${base} --inDir $(wav_dir)/wav --outDir $(out_dir)/wav >> $@_'
	mv $@_ $@	
	chmod +x $@
############################################
${out_dir}/wav/.done: ${out_dir}/wav/split.sh $(wav_dir)/.wav.done
	${out_dir}/wav/split.sh
	touch ${out_dir}/wav/.done
############################################
${out_dir}/extracted/metadata.csv: ${out_dir}/extracted/fixed.split.mlf
	pv $< | $(python_cmd) $(python_dir)/mlf_to_csv.py --outputPhones --skipSP > $@_
	mv $@_ $@
$(out_dir)/$(corpus)/metadata.csv: ${out_dir}/extracted/metadata.csv | $(out_dir)/$(corpus)
	pv $< | sed '/noise/d' | sort > $@_
	mv $@_ $@
$(out_dir)/$(corpus)/durations: ${out_dir}/extracted/fixed.split.mlf ${out_dir}/extracted/audio.samples \
	${out_dir}/extracted/exclude.files | $(out_dir)/$(corpus)
	pv $< | $(python_cmd) $(python_dir)/exclude_files.py --excludeFromFile ${out_dir}/extracted/exclude.files \
		| $(python_cmd) $(python_dir)/mlf_to_durations.py --shift 256 --freq 22050 --samplesFile ${out_dir}/extracted/audio.samples \
		| sort > $@_
	mv $@_ $@

############################################
${out_dir}/extracted/audio.samples: $(out_dir)/$(corpus)/wavs/.done
	ls -1 $(out_dir)/$(corpus)/wavs/*.wav | sort | pv | $(python_cmd) $(python_dir)/audio_to_samples.py > $@_
	mv $@_ $@
############################################
${out_dir}/extracted/exclude.files: ${out_dir}/extracted/metadata.csv
	cat $< | { grep 'noise' || test $$? = 1; } | awk -F'|' '{print $$1}' > $@_
	mv $@_ $@

############################################
$(wav_dir)/wav:
	mkdir -p $@
$(wav_dir)/.wav.extracted: $(wav_gz) | $(wav_dir)/wav
	tar -xf $< -C $(wav_dir)/wav
	touch $@
$(wav_dir)/.wav.done: $(wav_dir)/.wav.extracted
	cd $(wav_dir)/wav && (ls *.wav | xargs -I {} mv {} $(prefix)_{})
	touch $@	

############################################
$(out_dir)/$(corpus)/wavs/.done: ${out_dir}/extracted/initial.mlf ${out_dir}/wav/.done ${out_dir}/extracted/exclude.files | $(out_dir)/$(corpus)/wavs
	for wav in ${out_dir}/wav/*.wav; do \
		base=`basename $${wav} .wav`; \
		base=$$(echo $${base} | sed s/lab_//g); \
		echo "Copy wav $${base}"; \
		cp $${wav} $(out_dir)/$(corpus)/wavs/$${base}.wav; \
		# echo "Converting WAV to 22050 Hz 16 bit for $${base}"; \
		# sox $${wav} -r 22050 -b 16 $(out_dir)/$(corpus)/wavs/$${base}.wav; \
	done
	echo "Drop exluded files"
	cat ${out_dir}/extracted/exclude.files | xargs -n 1 -I {} sh -c 'rm $(out_dir)/$(corpus)/wavs/{}.wav'
	touch $(out_dir)/$(corpus)/wavs/.done
############################################
$(out_dir)/$(corpus).tar.gz: $(out_dir)/$(corpus)/wavs/.done $(out_dir)/$(corpus)/metadata.csv $(out_dir)/$(corpus)/durations
	tar -czf $(out_dir)/$(corpus).tar.gz -C $(out_dir)/ $(corpus)

############################################
test/durations: $(out_dir)/$(corpus)/durations
	cat $< | $(python_cmd) $(python_dir)/long_durations.py --duration 150
test/corpus-len: $(out_dir)/$(corpus)/wavs/.done
	ls -1 $(out_dir)/$(corpus)/wavs/*.wav | xargs -n1 soxi -D | $(python_cmd) -c "import sys; print(sum(float(x) for x in sys.stdin)/3600)"

$(bin):
	mkdir -p $(bin)
############################################
build-meta: $(out_dir)/$(corpus)/metadata.csv
build: $(out_dir)/$(corpus).tar.gz
test: ${out_dir}/range/.done
extract/wav: $(wav_dir)/.wav.extracted
############################################
############################################
clean:
	rm -rf $(out_dir)
clean/wav:
ifneq ($(force),1)	
	@echo -n "Drop $(out_dir)? Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
endif	
	rm -rf $(wav_dir)

.EXPORT_ALL_VARIABLES:	
