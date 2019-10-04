import React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Button, ActivityIndicator, Modal } from 'react-native';
import { Image, Icon } from 'react-native-elements';
import ImagePicker from 'react-native-image-crop-picker';
import { iOSColors } from 'react-native-typography';

import ImageViewer from 'react-native-image-zoom-viewer';
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
      '/Users/miguel/Library/Developer/CoreSimulator/Devices/F842241C-B2DF-40EA-B5C4-A396535A6B88/data/Containers/Data/Application/A611E372-A4F0-40EB-9234-7F75BECEB394/tmp/react-native-image-crop-picker/DC025A97-F223-4EA4-B5B0-5FFAF9973CF8.jpg',
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
          <Image
            style={styles.image}
            source={{ uri: photo.path }}
            placeholderStyle={styles.imagePlaceholder}
            resizeMode="cover"
            imagePlaceholder={<ActivityIndicator />}
          />
          // <Modal visible transparent>
          //   <ImageViewer
          //     saveToLocalByLongPress={false}
          //     enableSwipeDown
          //     imageUrls={[{ url: photo.path }]}
          //   />
          // </Modal>
          // <Image
          //   style={styles.image}
          //   source={{ uri: photo.path }}
          //   placeholderStyle={styles.imagePlaceholder}
          //   imagePlaceholder={<ActivityIndicator />}
          // />
        )}
      </View>
      <View style={styles.buttonContainer}>
        <Button
          title="Select image"
          onPress={() => {
            ImagePicker.openPicker({}).then(image => {
              console.log(`${new Date().toISOString()} - ScannerViewContainer:openPicker:image`);
              console.log(JSON.stringify(image));
              setPhoto(image);
            });
          }}
        />
        <Icon
          iconStyle={{ fontSize: 25 }}
          type="entypo"
          name="circle"
          color={iOSColors.black}
          size={13}
        />
        <Button title="Upload photo" onPress={handleUploadPhoto} />
        {/* <Button
          title="Go to Ticket"
          onPress={() => props.navigation.navigate('TicketView', { ticket })}
        /> */}
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
  },
  image: {
    ...styleDebug('red'),
    margin: 10,
    alignSelf: 'center',
    width: '60%',
    height: '100%',
  },
  imagePlaceholder: {
    backgroundColor: 'transparent',
  },
  buttonContainer: {
    ...styleDebug('blue'),
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
});

ScannerViewContainer.propTypes = {};
ScannerViewContainer.defaultProps = {};

export default ScannerViewContainer;
