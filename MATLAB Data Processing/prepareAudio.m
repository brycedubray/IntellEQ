function [filename,audio,Fs] = prepareAudio(file, path)
%prepareAudio Creates a vertical array of mono or stereo audio based
%             on the file chosen by user

[in, Fs] = audioread(path);
filename = file;
audio = in;
end

