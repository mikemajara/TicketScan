import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { StyleSheet, View, Button, Text, Image, Platform } from 'react-native';
import ImagePicker from 'react-native-image-crop-picker';


const createFormData = (photo, body) => {
  const data = new FormData();

  data.append('file', {
    name: "file",
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

  const handleUploadPhoto = () => {
    fetch('http://127.0.0.1:5000/api', {
      method: 'POST',
      body: createFormData(photo, { userId: '123' }),
    })
      .then(response => response.json())
      .then(response => {
        console.log('upload succes', response);
        console.log(response)
        setTicket(response);
        console.log(`${new Date().toISOString()} - ScannerViewContainer:handleUploadPhoto:response`);
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
      {photo && (
        <Image
          source={{ uri: photo.path }}
          style={{ width: 500, height: 500 }}
        />
      )}
      <Button
        title="Select image"
        onPress={() => {
          ImagePicker.openPicker({
          }).then(image => {
            setPhoto(image);
          });
        }}
      />
      <Button title="Upload photo" onPress={handleUploadPhoto} />
      <Button title="Go to Ticket" onPress={() => props.navigation.navigate('TicketView')} />
      <Text>{JSON.stringify(ticket, null, 2)}</Text>
    </View >
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
});

ScannerViewContainer.propTypes = {};
ScannerViewContainer.defaultProps = {};

export default ScannerViewContainer;
