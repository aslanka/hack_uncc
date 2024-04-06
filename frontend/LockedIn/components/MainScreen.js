import React from 'react';
import { View, Text, Button, StyleSheet, ScrollView, Image } from 'react-native';

const challenges = [
  { title: '#read a book a day', image: 'https://placehold.co/600x400' },
  { title: '#10 push ups a day', image: 'https://placehold.co/600x400' },
  // Add more challenges here
];

const MainScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <ScrollView>
        {challenges.map((challenge, index) => (
          <View key={index} style={styles.challenge}>
            <Text style={styles.title}>{challenge.title}</Text>
            <Button title="Subscribe" color="#232323" />
            <Image source={{ uri: challenge.image }} style={styles.image} resizeMode="cover" />
          </View>
        ))}
        <Button
          title="ADD your OWN"
          onPress={() => navigation.navigate('AddChallenge')}
          color="#232323"
        />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    backgroundColor: '#000',
  },
  challenge: {
    margin: 10,
    padding: 15,
    backgroundColor: '#232323',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#424242",
  },
  title: {
    color: 'white',
    fontSize: 16,
    marginBottom: 10,
  },
  image: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    resizeMode: 'cover', // Ensure the image covers the specified area
  },
});

export default MainScreen;
