import React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, ActivityIndicator, Text, Modal, Dimensions } from 'react-native';
import { Image, Icon, Button } from 'react-native-elements';
import ImagePicker from 'react-native-image-crop-picker';
import { iOSColors } from 'react-native-typography';
import ImageView from 'react-native-image-view';
import { TouchableOpacity } from 'react-native-gesture-handler';
import { styleDebug } from '../helpers';


const createFormData = (photo, body) => {
  const data = new FormData();

  data.append('file', {
    name: 'file',
    type: photo.type,
    uri: photo.path,
  });

  Object.keys(body).forEach(key => {
    data.append(key, body[key]);
  });

  return data;
};

const ScannerViewContainer = props => {
  const dummyPhoto = {
    exif: null,
    localIdentifier: 'D4A4EBEF-F4AE-48BA-B6E6-CA75FB4B0B3D/L0/001',
    filename: 'IMG_0020.JPG',
    width: 497,
    modificationDate: '1570028013',
    mime: 'image/jpeg',
    path:
      '/Users/miguel/Library/Developer/CoreSimulator/Devices/F842241C-B2DF-40EA-B5C4-A396535A6B88/data/Containers/Data/Application/FF35854C-C8AA-4649-93B6-D4E0C7A4520A/tmp/react-native-image-crop-picker/43EC9DF5-DA12-4328-A488-DC68E319DFE3.jpg',
    size: 136755,
    cropRect: null,
    data: null,
    sourceURL:
      'file:///Users/miguel/Library/Developer/CoreSimulator/Devices/F842241C-B2DF-40EA-B5C4-A396535A6B88/data/Media/DCIM/100APPLE/IMG_0020.JPG',
    height: 1544,
    creationDate: '1561211027',
  };

  const [ticket, setTicket] = useState({});
  const [photo, setPhoto] = useState(dummyPhoto);
  const [modalVisible, setModalVisible] = useState(false);

  const handleUploadPhoto = () => {
    fetch('http://127.0.0.1:5000/parse_ticket', {
      method: 'POST',
      body: createFormData(photo, { userId: '123' }),
    })
      .then(response => response.json())
      .then(response => {
        console.log('upload succes', response);
        console.log(response);
        setTicket(response);
        console.log(
          `${new Date().toISOString()} - ScannerViewContainer:handleUploadPhoto:response`
        );
        console.log(response);
        // props.navigation.navigate('TicketView', { elements: response })
        // setPhoto(null);
        // setTicket({});
      })
      .catch(error => {
        console.log('upload error', error);
        alert('Upload failed!');
      });
  };

  return (
    <View style={styles.container}>
      <View style={styles.imageContainer}>
        {photo && (
          <TouchableOpacity onPress={() => setModalVisible(true)}>
            <Image
              style={[styles.image, { width: 350, height: 550 }]}
              source={{ uri: photo.path }}
              placeholderStyle={styles.imagePlaceholder}
              resizeMode="contain"
              imagePlaceholder={<ActivityIndicator />}
            />
          </TouchableOpacity>
        )}
        <ImageView
          images={[
            {
              source: {
                uri: photo.path,
              },
              title: 'Mi ticket',
              width: photo.width / 2.5, // Don't know why it works better like this.
              height: photo.height / 2.5, // Maybe should be calculated dinamically
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
      </View>
      <View style={styles.bottomRow}>
        <View style={styles.buttonContainer}>
          <Button
            style={styles.buttonStyle}
            type="clear"
            title="Select image"
            onPress={() => {
              ImagePicker.openPicker({})
                .then(image => {
                  console.log(`${new Date().toISOString()} - ScannerViewContainer:openPicker:image`);
                  console.log(JSON.stringify(image));
                  setPhoto(image);
                })
                .catch(err => {
                  console.log(err);
                });
            }}
          />
          <Icon
            iconStyle={[styles.shutterButton, { fontSize: 50 }]}
            type="ionicon"
            name="ios-radio-button-on"
            color={iOSColors.black}
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
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    ...styleDebug('green'),
    flex: 1,
    justifyContent: 'center',
  },
  imageContainer: {
    ...styleDebug('orange'),
    margin: 10,
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
  }
});

ScannerViewContainer.propTypes = {};
ScannerViewContainer.defaultProps = {};

export default ScannerViewContainer;
