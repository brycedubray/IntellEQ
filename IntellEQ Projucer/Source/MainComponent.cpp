/*
  ==============================================================================

    This file was auto-generated!

  ==============================================================================
*/

#include "MainComponent.h"

//==============================================================================
MainComponent::MainComponent() : state(Stopped),
                                 thumbnailCache(5),
                                 thumbnail(512, formatManager, thumbnailCache)
{
    titleLabel.setText("IntellEQ - Intelligent Music Mastering", dontSendNotification);
    addAndMakeVisible(&titleLabel);
    
    addAndMakeVisible (&openButton);
    openButton.setButtonText ("Open File...");
    openButton.onClick = [this] { openButtonClicked(); };

    addAndMakeVisible (&playButton);
    playButton.setButtonText ("Play");
    playButton.onClick = [this] { playButtonClicked(); };
    playButton.setColour (juce::TextButton::buttonColourId, juce::Colours::green);
    playButton.setEnabled (false);
 
    addAndMakeVisible (&stopButton);
    stopButton.setButtonText ("Stop");
    stopButton.onClick = [this] { stopButtonClicked(); };
    stopButton.setColour (juce::TextButton::buttonColourId, juce::Colours::red);
    stopButton.setEnabled (false);
    
    formatManager.registerBasicFormats();
    transportSource.addChangeListener(this);
    
    thumbnail.addChangeListener (this);
    
    startTimer(40);
    
    setSize (800, 600);

    // Some platforms require permissions to open input channels so request that here
    if (RuntimePermissions::isRequired (RuntimePermissions::recordAudio)
        && ! RuntimePermissions::isGranted (RuntimePermissions::recordAudio))
    {
        RuntimePermissions::request (RuntimePermissions::recordAudio,
                                     [&] (bool granted) { if (granted)  setAudioChannels (2, 2); });
    }
    else
    {
        // Specify the number of input and output channels that we want to open
        setAudioChannels (2, 2);
    }
}

MainComponent::~MainComponent()
{
    // This shuts down the audio device and clears the audio source.
    shutdownAudio();
}

//==============================================================================
void MainComponent::prepareToPlay (int samplesPerBlockExpected, double sampleRate)
{
    transportSource.prepareToPlay(samplesPerBlockExpected, sampleRate);
}

void MainComponent::getNextAudioBlock (const AudioSourceChannelInfo& bufferToFill)
{
    if(readerSource.get() == nullptr)
    {
        bufferToFill.clearActiveBufferRegion();
        return;
    }
    
    transportSource.getNextAudioBlock(bufferToFill);
}

void MainComponent::releaseResources()
{
    transportSource.releaseResources();
}

//==============================================================================
void MainComponent::paint (Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (getLookAndFeel().findColour (ResizableWindow::backgroundColourId));
    
    Rectangle<int> thumbnailBounds (10, 200, getWidth() - 20, getHeight() - 400);
    if (thumbnail.getNumChannels() == 0)
        paintIfNoFileLoaded (g, thumbnailBounds);
    else
        paintIfFileLoaded (g, thumbnailBounds);
}

void MainComponent::resized()
{
    Rectangle<int> container = getLocalBounds();
    int w = container.getWidth()/6;
    int h = container.getHeight()/6;
    
    int margin = 10;
    
    int buttonWidth = getWidth()-(2*margin);
    int buttonHeight = 25;
    
    titleLabel.setBounds(2*w, 0, 500, 50);
    openButton.setBounds(margin, 1*h, buttonWidth, buttonHeight);
    stopButton.setBounds(margin, 1.25*h, buttonWidth, buttonHeight);
    playButton.setBounds(margin, 1.5*h, buttonWidth, buttonHeight);
}

//==============================================================================

void MainComponent::openButtonClicked() {
    juce::FileChooser chooser ("Select a Wave file to play...",
                                   {},
                                   "*.wav");
 
        if (chooser.browseForFileToOpen())
        {
            auto file = chooser.getResult();
            auto* reader = formatManager.createReaderFor (file);
 
            if (reader != nullptr)
            {
                std::unique_ptr<juce::AudioFormatReaderSource> newSource (new juce::AudioFormatReaderSource (reader, true));
                transportSource.setSource (newSource.get(), 0, nullptr, reader->sampleRate);
                playButton.setEnabled (true);
                thumbnail.setSource(new FileInputSource(file));
                readerSource.reset (newSource.release());
            }
        }
}

void MainComponent::playButtonClicked() {
    if ((state == Stopped) || (state == Paused))
        changeState(Starting);
    else if (state == Playing)
        changeState(Pausing);
}

void MainComponent::stopButtonClicked() {
    if (state == Paused)
            changeState (Stopped);
        else
            changeState (Stopping);
}

void MainComponent::changeListenerCallback (juce::ChangeBroadcaster* source) {
    if (source == &transportSource)
    {
        if (transportSource.isPlaying())
            changeState (Playing);
        else if ((state == Stopping || (state == Paused)))
            changeState (Stopped);
        else if (Pausing == state)
            changeState(Paused);
    }
    
    if (source == &thumbnail)
        thumbnailChanged();
}

void MainComponent::thumbnailChanged()
    {
        repaint();
    }

void MainComponent::changeState (TransportState newState)
    {
        if (state != newState)
        {
            state = newState;
 
            switch (state)
            {
                case Stopped:
                    playButton.setButtonText ("Play");
                    stopButton.setButtonText ("Stop");
                    stopButton.setEnabled (false);
                    transportSource.setPosition (0.0);
                    break;
 
                case Starting:
                    transportSource.start();
                    break;
 
                case Playing:
                    playButton.setButtonText ("Pause");
                    stopButton.setButtonText ("Stop");
                    stopButton.setEnabled (true);
                    break;
 
                case Pausing:
                    transportSource.stop();
                    break;
 
                case Paused:
                    playButton.setButtonText ("Resume");
                    stopButton.setButtonText ("Return to Zero");
                    break;
 
                case Stopping:
                    transportSource.stop();
                    break;
            }
        }
    }

void MainComponent::paintIfNoFileLoaded (juce::Graphics& g, const juce::Rectangle<int>& thumbnailBounds)
    {
        g.setColour (juce::Colours::darkgrey);
        g.fillRect (thumbnailBounds);
        g.setColour (juce::Colours::white);
        g.drawFittedText ("No File Loaded", thumbnailBounds, juce::Justification::centred, 1);
    }

void MainComponent::paintIfFileLoaded (juce::Graphics& g, const juce::Rectangle<int>& thumbnailBounds)
    {
        g.setColour (juce::Colours::darkgrey);
        g.fillRect (thumbnailBounds);
 
        g.setColour (juce::Colours::red);
        auto audioLength = (float) thumbnail.getTotalLength();
        thumbnail.drawChannels (g, thumbnailBounds, 0.0, audioLength, 1.0f);
        
        g.setColour(Colours::white);
        auto audioPosition = (float) transportSource.getCurrentPosition();
        auto drawPosition = (audioPosition/audioLength) * (float) thumbnailBounds.getWidth()
                            + (float) thumbnailBounds.getX();
        g.drawLine(drawPosition, (float) thumbnailBounds.getY(), drawPosition, (float) thumbnailBounds.getBottom(), 2.0f);
    }

void MainComponent::timerCallback() {
    repaint();
}
