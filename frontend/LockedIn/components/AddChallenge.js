import React, { useState } from 'react';
import { View, Text, Button, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as ImagePicker from 'expo-image-picker';

const api = axios.create({
  baseURL: `https://${process.env.EXPO_PUBLIC_API_LOGIN_API}`,
});

const AddChallengeScreen = () => {
  const [title, setTitle] = useState('');
  const [image, setImage] = useState(null);

  const createChallenge = async () => {
    try {
      const email = await AsyncStorage.getItem('userEmail');
      const response = await api.post('/create_challenge', {
        title: title,
        image: image,
        email: email,
      });
      alert(response.data.message);
    } catch (error) {
      console.error('Error creating challenge:', error);
      alert('Error creating challenge');
    }
  };

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status === 'granted') {
      let result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 1,
      });

      if (!result.cancelled) {
        setImage(result.uri);
      }
    }
  };

  const takePhoto = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status === 'granted') {
      let result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 1,
      });

      if (!result.cancelled) {
        setImage(result.uri);
      }
    }
  };

  return (
    <View style={styles.container}>
      <Text>Add your own challenge!</Text>
      <TextInput
        style={styles.input}
        placeholder="Challenge Title"
        value={title}
        onChangeText={setTitle}
      />
      <TouchableOpacity style={styles.button} onPress={pickImage}>
        <Text>Select Image from Library</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.button} onPress={takePhoto}>
        <Text>Take Photo</Text>
      </TouchableOpacity>
      <Button title="Create Challenge" onPress={createChallenge} disabled={!image || !title} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  input: {
    width: '100%',
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 10,
    marginBottom: 10,
  },
  button: {
    marginBottom: 10,
    padding: 10,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
});

export default AddChallengeScreen;
