import React from 'react';
import { View, Text, Button, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const challenges = [
  { title: '#drinkagallonofwater', image: 'https://placehold.co/600x400' },
  { title: '#donteatjunkfoodtoday', image: 'https://placehold.co/600x400' },
  // Add more challenges here
];

const MainScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      {/* Custom Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.toggleDrawer()}>
          <Ionicons name="menu" size={24} color="white" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>LockedIn</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Friends')}>
          <Ionicons name="people" size={24} color="white" />
        </TouchableOpacity>
      </View>
      {/* Main Content */}
      <ScrollView style={styles.content}>
        {challenges.map((challenge, index) => (
          <View key={index} style={styles.challenge}>
            <Text style={styles.title}>{challenge.title}</Text>
            <Button title="Subscribe" color="#232323" />
            <Image source={{ uri: challenge.image }} style={styles.image} resizeMode="cover" />
          </View>
        ))}
      </ScrollView>
      {/* Fixed Button */}
      <View style={styles.addButtonContainer}>
        <Button
          title="Post a challenge"
          onPress={() => navigation.navigate('AddChallenge')}
          color="black"
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  content: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#000',
    paddingTop: 35,
  },
  headerTitle: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
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
    resizeMode: 'cover',
  },
  addButtonContainer: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    right: 20,
    backgroundColor: '#02fff1',
    borderRadius: 10,
    marginBottom: 30,
  },
});

export default MainScreen;
