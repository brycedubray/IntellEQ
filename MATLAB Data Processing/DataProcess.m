
% IntellEQ Training Data Preparation Script
% Bryce DuBray
clc; clear; close all; clear sound;
% DataProcess.m

% This script takes an audio input array and outputs an array of length
% 5 representing the normalized amplitudes of 5 frequency bands of the
% input

% ENTER GENRE HERE
genre = "rock.";
filetype = ".wav";

counter = 0;
inputData = zeros(100, 5);

while counter < 100
    
    % Pad 0's to the beginning of the data file number
    if counter < 10
        zeroPad = "0000";
    else
        zeroPad = "000";
    end
    
    % assemble the appropriate filename
    fileNumber = zeroPad + int2str(counter);
    filename = genre + fileNumber + filetype;
    
    % Import audio file
    [in, Fs] = audioread(filename);
    
    % split audio into 5 bands
    
    in = upsample(in,2);   % upsample audio
    Fs = Fs * 2;
    
    % filter parameters
    Nyq = Fs/2;
    order = 2;                             % filter order
    numOfBands = 5;
    freq = [20, 250, 500, 2000, 6000, 20000];
       
    N = length(in);
    
    signalBands = zeros(N, numOfBands);  % initialize array for storage of filtered signals
    bandAmplitudes = zeros(1, numOfBands);
     
    for band = 1:numOfBands
        Wn = [freq(band) , freq(band+1)] ./ Nyq;
        [b,a] = butter(order,Wn);
        signalBands(:, band) = filter(b,a,in);
        
        % Calculate RMS of each band
        sigSquared = signalBands(:,band) .^2;
        sigMean = (1/N) * sum(sigSquared);
        sigRootSquared = sqrt(sigMean);
        bandAmplitudes(1,band) = sigRootSquared;
    end
    
    inputData(counter+1,:) = bandAmplitudes;
    
    counter = counter + 1
    
end