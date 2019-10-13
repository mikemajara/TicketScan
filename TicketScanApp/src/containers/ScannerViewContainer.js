import React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, ActivityIndicator, Text, Modal, Dimensions } from 'react-native';
import { Image, Icon, Button } from 'react-native-elements';
// FIXME: Crop picker not working after upgrade.
// import ImagePicker from 'react-native-image-crop-picker';
import { iOSColors } from 'react-native-typography';
import ImageView from 'react-native-image-view';
import { TouchableOpacity } from 'react-native-gesture-handler';
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
      // .then(response => response.json())
      .then(response => {
        setLoading(false);
        // setTicket(response);
        // Navigate to ticket with correct response
        props.navigation.navigate('TicketView', { elements: response })
        // setImage(null);
        // setTicket({});
      })
      .catch(error => {
        setLoading(false);
        console.log('upload error', error);
        alert('Upload failed!');
      })
      .finally(() => setLoading(false));
  };

  return (
    <View style={styles.container}>
      {/* <View style={{ ...styleDebug('red'), borderWidth: 3 }}> */}
      {/* <DocumentScanner
          useBase64
          saveInAppDocument={false}
          onPictureTaken={data =>
            setImage({
              image: data.croppedImage,
              initialImage: data.initialImage,
              rectangleCoordinates: data.rectangleCoordinates
            })
          }
          overlayColor="rgba(255,130,0, 0.7)"
          enableTorch={false}
          brightness={0.3}
          saturation={1}
          contrast={1.1}
          quality={0.5}
          onRectangleDetect={({ stableCounter, lastDetectionType }) =>
            setDocumentInfo({ stableCounter, lastDetectionType })
          }
          detectionCountBeforeCapture={5}
          detectionRefreshRateInMS={50}
          onPermissionsDenied={() => console.log('Permissions Denied')}
        />
        {image && <Image source={{ uri: `data:image/jpeg;base64,${image}` }} resizeMode="contain" />} */}
      {/* </View> */}
      {loading && (
        <LoadingComponent
          isLoading={loading}
          loadingText="Your ticket is being read by our staff..."
        />)
      }
      <View style={[styles.imageContainer, { padding: image ? 10 : 0 }]}>
        {
          image ?
            <View>
              {/* <Image
                style={{ width: 400, height: 400 }}
                source={{ uri: `data:image/jpeg;base64,${image}` }}
                resizeMode="contain"
              /> */}
              <TouchableOpacity onPress={() => setModalVisible(true)}>
                <Image
                  style={[styles.image, { width: 400, height: 400 }]}
                  source={{ uri: image.path || `data:image/jpeg;base64,${image}` }}
                  placeholderStyle={styles.imagePlaceholder}
                  resizeMode="contain"
                  imagePlaceholder={<ActivityIndicator />}
                />
              </TouchableOpacity>
              <ImageView
                images={[
                  {
                    source: {
                      uri: image.path || `data:image/jpeg;base64,${image}`,
                    },
                    title: 'Mi ticket',
                    width: image.width / 2.5, // Don't know why it works better like this.
                    height: image.height / 2.5, // Maybe should be calculated dinamically
                  },
                ]}
                controls={{ close: null }}
                onClose={() => {
                  setModalVisible(false);
                }}
                animationType="fade"
                imageIndex={0}
                isVisible={modalVisible}
              />
            </View> :
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
          // onPress={() => {
          //   ImagePicker.openPicker({})
          //     .then(image => {
          //       setImage(image);
          //     })
          //     .catch(err => {
          //       console.log(err);
          //     });
          // }}
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
