import React, { useState } from 'react';
import { View, Text, Button, TextInput, StyleSheet } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: `https://${process.env.EXPO_PUBLIC_API_LOGIN_API}`,
});

const AddChallengeScreen = () => {
  const [title, setTitle] = useState('');
  const [image, setImage] = useState('');

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

  return (
    <View style={styles.container}>
      <Text>Add your own challenge!</Text>
      <TextInput
        style={styles.input}
        placeholder="Challenge Title"
        value={title}
        onChangeText={setTitle}
      />
      <TextInput
        style={styles.input}
        placeholder="Image URL"
        value={image}
        onChangeText={setImage}
      />
      <Button title="Create Challenge" onPress={createChallenge} />
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
});

export default AddChallengeScreen;
