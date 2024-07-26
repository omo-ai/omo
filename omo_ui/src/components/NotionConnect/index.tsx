import React, { useEffect, useState } from 'react';
import qs from 'qs';
import useSWR from 'swr';
import { buildApiUrl } from '@/utils/api';
import { stringify } from 'querystring';
import { url } from 'inspector';
import { headers } from 'next/headers';

type NotionConnectButtonProps = {
  authUrl: string;
}

const NotionConnectButton = ( { authUrl }: NotionConnectButtonProps) => {

  const handleLogin = () => {
    window.location.href = authUrl;
  };

  return (
    <div>
      <button className="btn-stroke-light w-full mt-8 md:mt-6" onClick={handleLogin}>Connect to Notion</button>
    </div>
  );
};

export default NotionConnectButton;