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

  const [ticket, setTicket] = useState({});
  const [photo, setPhoto] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const handleUploadPhoto = () => {
    fetch('http://127.0.0.1:5000/parse_ticket', {
      method: 'POST',
      body: createFormData(photo, { userId: '123' }),
    })
      .then(response => response.json())
      .then(response => {
        setTicket(response);
        // Navigate to ticket with correct response
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
                  setPhoto(image);
                })
                .catch(err => {
                  console.log(err);
                });
            }}
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
