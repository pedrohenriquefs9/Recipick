import React, { useState, useRef, useEffect } from 'react';
import { PlusIcon, MagnifyingGlassIcon, Bars3Icon, EllipsisVerticalIcon, StarIcon, TrashIcon, Cog6ToothIcon, PencilIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';

function ChatOptionsMenu({ onFavorite, onRemove, onOpenSettings, onRename, isFavorite, isFavoriteDisabled }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    // Adiciona o listener quando o menu está aberto
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    // Função de limpeza para remover o listener
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]); // O efeito depende do estado 'isOpen'

  return (
    <div className="relative" ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)} className="p-1 rounded-full hover:bg-gray-200">
        <EllipsisVerticalIcon className="h-5 w-5 text-gray-500" />
      </button>
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 ring-1 ring-black ring-opacity-5">
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
      onSave(currentTitle); // Reverte se o título ficar vazio
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSave();
    }
    if (e.key === 'Escape') {
      onSave(currentTitle); // Cancela a edição
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

  const favoriteChats = chats.filter(chat => chat.isFavorite);
  
  // A lógica de filtro agora só se aplica aos chats que NÃO são favoritos.
  const filteredHistoryChats = chats.filter(chat =>
    !chat.isFavorite && chat.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const renderChatList = (chatList, title, emptyMessage) => (
    <div className="mb-4">
      <h3 className="px-4 text-sm font-semibold text-gray-500 mb-2">{title}</h3>
      {chatList.length > 0 ? (
        <ul>
          {chatList.map(chat => (
            chat.id && (
              <li key={chat.id} className={`flex items-center justify-between p-2 px-4 rounded-lg mx-2 cursor-pointer ${activeChatId === chat.id ? 'bg-primary bg-opacity-20' : 'hover:bg-gray-100'}`}>
                <div className="flex-grow mr-2 truncate" onClick={() => onSelectChat(chat.id)}>
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
    <div className={`flex flex-col h-full bg-white shadow-lg transition-all duration-300 ${isSidebarOpen ? 'w-72' : 'w-0'}`}>
      <div className={`p-4 border-b flex justify-between items-center ${!isSidebarOpen && 'hidden'}`}>
        <h2 className="text-xl font-bold text-primary-dark">ReciPick</h2>
        <button onClick={() => setIsSidebarOpen(false)} className="p-1 rounded-md hover:bg-gray-200">
          <Bars3Icon className="h-6 w-6" />
        </button>
      </div>
      <div className={`p-4 ${!isSidebarOpen && 'hidden'}`}>
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
      <div className={`flex-grow overflow-y-auto ${!isSidebarOpen && 'hidden'}`}>
        {}
        {renderChatList(favoriteChats, "Favoritos", "Nenhum favorito.")}
        {renderChatList(filteredHistoryChats, "Histórico de pedidos", searchTerm ? "Nenhum pedido encontrado." : "Nenhum pedido no histórico.")}
      </div>
    </div>
  );
}