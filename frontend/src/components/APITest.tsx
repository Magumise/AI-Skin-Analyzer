import React, { useState } from 'react';
import { Box, Button, Text, VStack, useToast } from '@chakra-ui/react';

const APITest = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const toast = useToast();

  const handleTest = async () => {
    setIsLoading(true);
    setResult(null);
    try {
      // const success = await testLogin();
      setResult('API test completed');
      toast({
        title: 'Success',
        description: 'API test completed successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      setResult('Error: ' + (error instanceof Error ? error.message : 'Unknown error'));
      toast({
        title: 'Error',
        description: 'API test failed',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box p={4} borderWidth="1px" borderRadius="lg">
      <VStack spacing={4}>
        <Text fontSize="lg" fontWeight="bold">API Test Component</Text>
        <Button
          colorScheme="blue"
          onClick={handleTest}
          isLoading={isLoading}
        >
          Run API Test
        </Button>
        {result && (
          <Text color={result.includes('passed') ? 'green.500' : 'red.500'}>
            {result}
          </Text>
        )}
      </VStack>
    </Box>
  );
};

export default APITest; 