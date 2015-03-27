FROM ubuntu

RUN echo "source ~/.bashrc" >> ~/.bash_profile

# General dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    tmux \
    unzip \
    wget

ENV HOME /root
WORKDIR $HOME

# Install SDK
ENV SDKNAME Neurotec_Biometric_5_1_SDK_Trial
RUN wget -O tmp.zip http://download.neurotechnology.com/$SDKNAME\_2015-03-02.zip && \
    unzip tmp.zip && \
    rm tmp.zip && \
# Only keep the files we need and remove the rest
    mkdir -p \
      sdk/Bin \
      sdk/Lib \
      sdk/Tutorials/Biometrics \
      sdk/Tutorials/Common && \
    mv $SDKNAME/Bin/Data sdk/Bin/Data && \
    mv $SDKNAME/Bin/Linux_x86_64 sdk/Bin/Linux_x86_64 && \
    mv $SDKNAME/Lib/Linux_x86_64 sdk/Lib/Linux_x86_64 && \
    mv $SDKNAME/Tutorials/Biometrics/C sdk/Tutorials/Biometrics/C && \
    mv $SDKNAME/Tutorials/Common/Build $SDKNAME/Tutorials/Common/C \
       -t sdk/Tutorials/Common && \
    mv $SDKNAME/Include sdk/Include && \
    rm -r $SDKNAME
RUN echo "export LD_LIBRARY_PATH=$HOME/sdk/Lib/Linux_x86_64" > ~/.bashrc

# Build Tutorials
RUN sdk/Bin/Linux_x86_64/Activation/run_pgd.sh start && \
    cd sdk/Tutorials/Biometrics/C && \
    make -C EnrollFaceFromCamera && \
    make -C Identify

# Copy binaries
RUN cp -r sdk/Bin/Linux_x86_64/Activation $HOME/bin && \
    cp sdk/Bin/Data/Faces.ndf -t $HOME/bin && \
    cd sdk/Tutorials/Biometrics/C && \
    cp EnrollFaceFromCamera/.obj/release/Linux_x86_64/EnrollFaceFromCamera/EnrollFaceFromCamera -t $HOME/bin && \
    cp Identify/.obj/release/Linux_x86_64/Identify/Identify -t $HOME/bin

# Copy libraries
RUN cp -r sdk/Lib/Linux_x86_64 lib
