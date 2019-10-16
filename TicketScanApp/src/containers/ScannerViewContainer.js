import React from 'react';
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, ActivityIndicator, Text, Modal, Dimensions } from 'react-native';
import { Image, Icon, Button } from 'react-native-elements';
import ImagePicker from 'react-native-image-picker';
import { iOSColors } from 'react-native-typography';
import { TouchableOpacity } from 'react-native-gesture-handler';
import ImageView from 'react-native-image-view';
import Scanner from 'react-native-document-scanner';

import { styleDebug } from '../helpers';
import LoadingComponent from '../components/LoadingComponent';

const createFormData = (image, body) => {
  const data = new FormData();

  data.append('file', {
    name: 'file',
    type: image.type,
    uri: image.path,
  });

  Object.keys(body).forEach(key => {
    data.append(key, body[key]);
  });

  return data;
};

const ScannerViewContainer = props => {

  // const [ticket, setTicket] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState(null);
  const [documentInfo, setDocumentInfo] = useState({});

  const handleUploadPhoto = () => {
    setLoading(true);
    console.log('uploading image...')
    fetch('http://127.0.0.1:5000/parse_ticket', {
      method: 'POST',
      body: createFormData(image, { userId: '123' }),
    })
      .then(response => response.json())
      .then(response => {
        setLoading(false);

        // TODO: REMOVE TRACE
        console.log(`${new Date().toISOString()} - ScannerViewContainer:49:response`);
        console.log(response);
        // ^^^^^ REMOVE TRACE

        // Navigate to ticket with correct response
        props.navigation.navigate('TicketView', { ticket: response });
        // setImage(null);
        // setTicket({});
      })
      .catch(error => {
        setLoading(false);
        console.log('upload error', error);
        Alert.alert('Upload failed!');
      })
      .finally(() => setLoading(false));
  };

  // More info on all the options is below in the API Reference... just some common use cases shown here
  const options = {
    title: 'Select scanned image',
    storageOptions: {
      skipBackup: true,
      path: 'images',
    },
  };

  const handleImagePicker = e => {
    // * The first arg is the options object for customization (it can also be null or omitted for default options),
    // * The second arg is the callback which sends object: response (more info in the API Reference)
    // */
    ImagePicker.launchImageLibrary(options, (response) => {
      console.log('Response = ', response);

      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      } else {
        const source = { path: response.uri };

        // You can also display the image using data:
        // const source = { uri: 'data:image/jpeg;base64,' + response.data };
        setImage(source);
      }
    });
  };

  useEffect(() => {

    // TODO: REMOVE TRACE
    console.log(`${new Date().toISOString()} - ScannerViewContainer:96:image`);
    console.log(image);
    // ^^^^^ REMOVE TRACE

  });

  return (
    <View style={styles.container}>
      {loading && (
        <LoadingComponent
          isLoading={loading}
          loadingText="Your ticket is being read by our staff..."
        />)
      }
      <View style={[styles.imageContainer, { padding: image ? 10 : 0 }]}>
        {
          image ?
            <Image
              style={[styles.image, { width: 400, height: 500 }]}
              source={{ uri: image.path || `data:image/jpeg;base64,${image}` }}
              placeholderStyle={styles.imagePlaceholder}
              resizeMode="contain"
              imagePlaceholder={<ActivityIndicator />}
            /> :
            <Scanner
              style={styles.scanner}
              useBase64
              onPictureTaken={data => {
                setImage(data.croppedImage);
              }}
              overlayColor="rgba(255,130,0, 0.7)"
              // enableTorch={this.state.flashEnabled}
              // useFrontCam={this.state.useFrontCam}
              brightness={0.2}
              saturation={0}
              quality={0.5}
              contrast={1.2}
              // onRectangleDetect={({ stableCounter, lastDetectionType }) => this.setState({ stableCounter, lastDetectionType })}
              detectionCountBeforeCapture={10}
              detectionRefreshRateInMS={50}
            />
        }
      </View>
      <View style={styles.bottomRow}>
        <View style={styles.buttonContainer}>
          <Button
            style={styles.buttonStyle}
            type="clear"
            title="Select image"
            onPress={handleImagePicker}
          />
          <Icon
            iconStyle={[styles.shutterButton, { opacity: 0.75, fontSize: 50 }]}
            type="ionicon"
            name="ios-radio-button-on"
            color={iOSColors.blue}
            size={13}
          />
          <Button
            style={styles.buttonStyle}
            type="clear"
            title="Upload photo"
            disabled={image == null}
            onPress={handleUploadPhoto}
          />
          {/* <Button
          title="Go to Ticket"
          onPress={() => props.navigation.navigate('TicketView', { ticket })}
        /> */}
        </View>
      </View>
    </View >
  );
};

const styles = StyleSheet.create({
  container: {
    ...styleDebug('green'),
    flex: 1,
    justifyContent: 'center',
  },
  imageContainer: {
    ...styleDebug('red'),
    backgroundColor: iOSColors.customGray,
    flex: 8,
    flexDirection: 'row',
    justifyContent: 'center',
  },
  image: {
    ...styleDebug('red'),
  },
  imagePlaceholder: {
    backgroundColor: 'transparent',
  },
  shutterButton: {
    ...styleDebug('purple'),
    padding: 8,
  },
  bottomRow: {
    borderTopColor: iOSColors.black,
    borderTopWidth: StyleSheet.hairlineWidth,
    flex: 2,
    justifyContent: 'center',
    paddingHorizontal: 10,
  },
  buttonContainer: {
    ...styleDebug('blue'),
    flexDirection: 'row',
    justifyContent: 'center',
  },
  buttonStyle: {
    ...styleDebug('red'),
    marginVertical: 10,
    width: 150,
  },
  scanner: {
    ...styleDebug('orange'),
    borderWidth: 3,
    flex: 1,
    width: '100%',
    height: '100%',
  }
});

ScannerViewContainer.propTypes = {};
ScannerViewContainer.defaultProps = {};

export default ScannerViewContainer;
