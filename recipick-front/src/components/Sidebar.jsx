import React, { useState, useRef, useEffect } from 'react';
import { PlusIcon, MagnifyingGlassIcon, Bars3Icon, EllipsisVerticalIcon, StarIcon, TrashIcon, Cog6ToothIcon, PencilIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import clsx from 'clsx';

function ChatOptionsMenu({ onFavorite, onRemove, onOpenSettings, onRename, isFavorite, isFavoriteDisabled }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="relative" ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)} className="p-1 rounded-full hover:bg-gray-200">
        <EllipsisVerticalIcon className="h-5 w-5 text-gray-500" />
      </button>
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-20 ring-1 ring-black ring-opacity-5">
          <button
            onClick={() => { onRename(); setIsOpen(false); }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <PencilIcon className="h-5 w-5 mr-3" />
            Renomear
          </button>
          <button
            onClick={() => { onOpenSettings(); setIsOpen(false); }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <Cog6ToothIcon className="h-5 w-5 mr-3" />
            Configurações
          </button>
          <button
            onClick={() => { onFavorite(); setIsOpen(false); }}
            disabled={isFavoriteDisabled}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isFavorite ? <StarIconSolid className="h-5 w-5 mr-3 text-yellow-500" /> : <StarIcon className="h-5 w-5 mr-3" />}
            {isFavorite ? 'Desfavoritar' : 'Favoritar'}
          </button>
          <button
            onClick={() => { onRemove(); setIsOpen(false); }}
            className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <TrashIcon className="h-5 w-5 mr-3" />
            Remover
          </button>
        </div>
      )}
    </div>
  );
}

function RenameInput({ currentTitle, onSave }) {
  const [title, setTitle] = useState(currentTitle);
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
    inputRef.current?.select();
  }, []);

  const handleSave = () => {
    if (title.trim()) {
      onSave(title.trim());
    } else {
      onSave(currentTitle);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSave();
    }
    if (e.key === 'Escape') {
      onSave(currentTitle);
    }
  };

  return (
    <input
      ref={inputRef}
      type="text"
      value={title}
      onChange={(e) => setTitle(e.target.value)}
      onBlur={handleSave}
      onKeyDown={handleKeyDown}
      className="w-full bg-transparent border border-primary rounded-md px-1 py-0 text-sm outline-none"
    />
  );
}

export function Sidebar({
  chats,
  activeChatId,
  onNewChat,
  onSelectChat,
  onFavoriteChat,
  onRemoveChat,
  onOpenSettings,
  isSidebarOpen,
  setIsSidebarOpen,
  renamingChatId,
  onRenameChat,
  onSaveChatTitle
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const sidebarRef = useRef(null);

  const favoriteChats = chats.filter(chat => chat.isFavorite);
  const filteredHistoryChats = chats.filter(chat =>
    !chat.isFavorite && chat.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelectChatAndClose = (id) => {
    onSelectChat(id);
    if (window.innerWidth < 1024) {
      setIsSidebarOpen(false);
    }
  };
  
  const renderChatList = (chatList, title, emptyMessage) => (
    <div className="mb-4">
      <h3 className="px-4 text-sm font-semibold text-gray-500 mb-2">{title}</h3>
      {chatList.length > 0 ? (
        <ul>
          {chatList.map(chat => (
            chat.id && (
              <li key={chat.id} className={clsx('flex items-center justify-between p-2 px-4 rounded-lg mx-2 cursor-pointer', {
                'bg-primary bg-opacity-20': activeChatId === chat.id,
                'hover:bg-gray-100': activeChatId !== chat.id
              })}>
                <div className="flex-grow mr-2 truncate" onClick={() => handleSelectChatAndClose(chat.id)}>
                  {renamingChatId === chat.id ? (
                    <RenameInput currentTitle={chat.title} onSave={(newTitle) => onSaveChatTitle(chat.id, newTitle)} />
                  ) : (
                    <span className="truncate">{chat.title || 'Novo Pedido'}</span>
                  )}
                </div>
                <ChatOptionsMenu
                  isFavorite={chat.isFavorite}
                  isFavoriteDisabled={chat.id.toString().startsWith('local-')}
                  onFavorite={() => onFavoriteChat(chat.id)}
                  onRemove={() => onRemoveChat(chat.id)}
                  onOpenSettings={() => onOpenSettings(chat.id)}
                  onRename={() => onRenameChat(chat.id)}
                />
              </li>
            )
          ))}
        </ul>
      ) : (
        <p className="px-4 text-sm text-gray-400">{emptyMessage}</p>
      )}
    </div>
  );

  return (
    <div 
      ref={sidebarRef}
      className={clsx(
        'flex-shrink-0 flex flex-col h-full bg-white shadow-lg transition-all duration-300 ease-in-out',
        'fixed lg:relative z-40', // Base para ambos os layouts
        {
          'translate-x-0 w-72': isSidebarOpen, // Aberto (mobile e desktop)
          '-translate-x-full lg:translate-x-0 lg:w-0': !isSidebarOpen // Fechado (lógica separada para mobile e desktop)
        }
      )}
    >
      <div className={clsx('w-72 h-full flex flex-col flex-shrink-0', !isSidebarOpen && 'lg:hidden')}>
        <div className="p-4 border-b flex justify-between items-center flex-shrink-0">
          <h2 className="text-xl font-bold text-primary-dark">ReciPick</h2>
          <button onClick={() => setIsSidebarOpen(false)} className="p-1 rounded-md hover:bg-gray-200">
              <Bars3Icon className="h-6 w-6" />
          </button>
        </div>
        <div className="p-4 flex-shrink-0">
          <button
              onClick={onNewChat}
              className="w-full flex items-center justify-center gap-2 p-2 rounded-full bg-primary text-light font-semibold mb-4 hover:bg-primary-dark transition-colors"
          >
              <PlusIcon className="h-5 w-5" />
              Fazer novo pedido
          </button>
          <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
              type="text"
              placeholder="Pesquisar..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-full bg-solid border border-transparent focus:outline-none focus:ring-2 focus:ring-primary"
              />
          </div>
        </div>
        <div className="flex-grow overflow-y-auto">
          {renderChatList(favoriteChats, "Favoritos", "Nenhum favorito.")}
          {renderChatList(filteredHistoryChats, "Histórico de pedidos", searchTerm ? "Nenhum pedido encontrado." : "Nenhum pedido no histórico.")}
        </div>
      </div>
    </div>
  );
}